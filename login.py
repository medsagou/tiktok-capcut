import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils import config

# Huge credits to redianmarku
# https://github.com/redianmarku/tiktok-autouploader

def upload_to_tiktok():
    print("init the bot")
    bot = utils.create_bot() # Might not work in headless mode
    print("adjusting the window")
    bot.set_window_size(1920, 1080*2) # Ensure upload button is visible, does not matter if it goes off screen

    # Fetch main page to load cookies, sometimes infinte loads, except and pass to keep going
    print("getting the site")
    try:
        bot.get('https://www.tiktok.com/')
    except:
        pass
    # print("writing the cookies")
    # for cookie in config['tiktok_cookies'].split('; '):
    #     data = cookie.split('=')
    #     bot.add_cookie({'name':data[0],'value':data[1]})
    # print("getting the upload site")
    # try:
    #     bot.get('https://www.tiktok.com/upload')
    # except:
    #     pass
    time.sleep(1)

    try:
        bot.get('https://www.tiktok.com/login')
    except:
        pass
    time.sleep(1)

    try:
        bot.get('https://www.tiktok.com/login/phone-or-email')
    except:
        pass

    try:
        bot.get("https://www.tiktok.com/login/phone-or-email/email")
    except:
        pass

    user_name = WebDriverWait(bot, 1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    print("writing user name..")

    user_name.send_keys("jcjdkmytt7t ")

    password = WebDriverWait(bot, 1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))

    password.send_keys("Picturesediting1.")
    print("password done")
    ActionChains(bot).send_keys(Keys.RETURN).perform()
    print("button returned")
    time.sleep(1000)
    bot.close()
    # time.sleep(20000)






if __name__=='__main__':
    for i in range(10):
        print(i)
        upload_to_tiktok()