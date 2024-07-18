import yaml
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium import webdriver
import seleniumwire.undetected_chromedriver as uc
import random
import string
# from selenium.webdriver.firefox.options import Options
# import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from seleniumwire import webdriver
import os
# Load and validate config
config = yaml.safe_load(open('config.yaml').read())

# if not config['tiktok_cookies']:
#     raise Exception('Missing TikTok Cookies')

# if not config['reddit_cookies']:
#     raise Exception('Missing Reddit Cookies')

def create_bot(headless=False):
    if not config['firefox']:
        options = uc.ChromeOptions()
        # options = webdriver.ChromeOptions()

        option_slwr={'disable_capture': True}
        options.add_argument("--log-level=3")
        options.add_argument('--disable-features=PrivacySandboxSettings4')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-extensions')
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")

        # options.headless = True
        prefs = {'profile.default_content_setting_values': { 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument('disable-infobars')

        seleniumwire_options = {
            'disable_encoding': True,
            'verify_ssl': False,
            'ignore_http_methods': ['GET', 'OPTIONS']
        }


        # bot = webdriver.Firefox(firefox_profile)
        bot = uc.Chrome(options=options, seleniumwire_options=seleniumwire_options, executable_path=os.getcwd() + "\\chromedriver.exe")
        # bot = webdriver.Chrome(options=options)
        # bot.scopes = ['.*edit-api-sg.capcut.*']
    else:
        bot = webdriver.Firefox()
    
    bot.maximize_window()
    # bot.set_page_load_timeout(25)
    # bot.set_window_size(1024, 768)
    return bot


def check_close_btn(bot):
    try:
        close_btn = WebDriverWait(bot, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[class^='guide-close-icon-']")))
    except Exception as e:
        print('we didnt find the close button')
        # print(e)
    else:
        print("we've find the close button")
        try:
            close_btn.click()
        except Exception as e:
            print("an exception", e)
        check_close_btn(bot)

def get_request(bot):
    while True:
        print("Start Searching now!!")
        for req in bot.requests:
            print(req.url)
            if 'publish_asset_to_third_party_platform' in req.url:
                print(req.url)
                return req
            

def handle_auth_tiktok(bot, main_tiktok_page, main_capcut_page):
    for handle in bot.window_handles:
            if handle != main_tiktok_page and handle != main_capcut_page:
                login_page = handle
                break

    # change the control to signin page
    bot.switch_to.window(login_page)
    print("switched to login with tiktok popup...")
    print("finding the Continue button")
    try:
        continue_button = WebDriverWait(bot, 100).until(
            EC.element_to_be_clickable((By.ID, "auth-btn"))
        )
        # continue_button = WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.XPATH, '//button[div/div[text()="Continue"]]')))
    except Exception as e:
        # print(e)
        print('we didnt find the Continue button...')
        print("but we will continue!")
        try:
            bot.switch_to.window(main_capcut_page)
        except:
            pass
        try:
            # Wait until the "Welcome to CapCut" text is not present in the page
            WebDriverWait(bot, 10).until(
                EC.invisibility_of_element((By.XPATH, "//*[text()='Welcome to CapCut']"))
            )
            print("The 'Welcome to CapCut' text is no longer present on the page.")
        except:
            print("Timed out waiting for 'Welcome to CapCut' text to disappear.")
            handle_login_element(bot, main_tiktok_page, main_cacpcut_page)
        check_close_btn(bot)
        try:
            WebDriverWait(bot, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".lv-avatar-image"))
        )
        except Exception as e:
            print("I think we didnt login but we will continue", e)
        check_close_btn(bot)
        # time.sleep(2000)
        # time.sleep(2)
        # print(bot.page_source)

    else:
        continue_button.click()
        print("Continue Button FOUND AND CLICKED!")
        
        # print("Switching to capcut main page")
        try:
            print("waiting to automaticly close the windows")
            WebDriverWait(bot, 30).until(lambda d: len(d.window_handles) == 2)
            bot.switch_to.window(main_capcut_page)
        except:
            print("there three windows, I dont know what to do")
            # bot.switch_to.window(handle)
            bot.close()
            bot.switch_to.window(main_capcut_page)
            return False
        return True
            


def text_aleatoire():
    length = random.randint(8, 16)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def handle_login_element(bot, main_tiktok_page, main_cacpcut_page):
    try:
        span_element = WebDriverWait(bot, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='{}']".format('Continue with TikTok'))
            )
        )
    except:
        print('error')
        pass
    else:
        print("Span with text 'Continue with TikTok' found!")
        span_element.click()
        w = handle_auth_tiktok(bot=bot, main_tiktok_page=main_tiktok_page, main_capcut_page=main_cacpcut_page)
        if not w:  
            handle_login_element(bot, main_tiktok_page, main_cacpcut_page)
        try:
            # Wait until the "Welcome to CapCut" text is not present in the page
            WebDriverWait(bot, 10).until(
                EC.invisibility_of_element((By.XPATH, "//*[text()='Welcome to CapCut']"))
            )
            print("The 'Welcome to CapCut' text is no longer present on the page.")
        except:
            print("Timed out waiting for 'Welcome to CapCut' text to disappear.")
            handle_login_element(bot, main_tiktok_page, main_cacpcut_page)