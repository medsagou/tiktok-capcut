import yaml
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import seleniumwire.undetected_chromedriver as uc
import random
import string
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Load and validate config
config = yaml.safe_load(open('config.yaml').read())

# if not config['tiktok_cookies']:
#     raise Exception('Missing TikTok Cookies')

# if not config['reddit_cookies']:
#     raise Exception('Missing Reddit Cookies')

def create_bot(headless=False):
    options = uc.ChromeOptions()
    option_slwr={'disable_capture': True}
    options.add_argument("--log-level=3")
    options.add_argument('--disable-features=PrivacySandboxSettings4')
    # options.add_argument('disable-infobars')
    if headless:
        options.headless = True

    bot = uc.Chrome(options=options)
    bot.scopes = ['.*edit-api-sg.capcut.*']
    

    # bot.set_page_load_timeout(25)
    bot.set_window_size(1920, 1080)
    return bot


def check_close_btn(bot):
    try:
        close_btn = WebDriverWait(bot, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class^='guide-close-icon-']")))
    except:
        print('error finding the close button')
    else:
        print("we've find the close button")
        close_btn.click()
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
            EC.presence_of_element_located((By.ID, "auth-btn"))
        )
    except Exception as e:
        # print(e)
        print('error, finding the Continue button...')
        print("but we will continue!")
        bot.switch_to.window(main_capcut_page)
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
        
        print("Switching to capcut main page")
        bot.switch_to.window(main_capcut_page)
        try:
            print("waiting to automaticly close the windows")
            WebDriverWait(bot, 100).until(lambda d: len(d.window_handles) == 2)
        except:
            print("there three windows, I dont know what to do")
            


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
        handle_auth_tiktok(bot=bot, main_tiktok_page=main_tiktok_page, main_capcut_page=main_cacpcut_page)
        try:
            # Wait until the "Welcome to CapCut" text is not present in the page
            WebDriverWait(bot, 20).until(
                EC.invisibility_of_element((By.XPATH, "//*[text()='Welcome to CapCut']"))
            )
            print("The 'Welcome to CapCut' text is no longer present on the page.")
        except:
            print("Timed out waiting for 'Welcome to CapCut' text to disappear.")
            handle_login_element(bot, main_tiktok_page, main_cacpcut_page)