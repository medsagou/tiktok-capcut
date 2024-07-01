import yaml
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Load and validate config
config = yaml.safe_load(open('config.yaml').read())

if not config['tiktok_cookies']:
    raise Exception('Missing TikTok Cookies')

if not config['reddit_cookies']:
    raise Exception('Missing Reddit Cookies')

def create_bot(headless=False):
    options = uc.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument('--disable-features=PrivacySandboxSettings4')
    # options.add_argument('disable-infobars')
    if headless:
        options.headless = True

    bot = uc.Chrome(options=options)

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