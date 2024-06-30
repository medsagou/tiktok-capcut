import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui


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
        bot.get('https://www.capcut.com/signup')
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
    main_page = bot.current_window_handle
    try:
        span_element = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='{}']".format('Continue with TikTok'))
            )
        )
    except:
        print('error')
        pass
    else:
        print("Span with text 'Continue with TikTok' found!")

        # Optionally, you can click on the span if needed
        span_element.click()

    for handle in bot.window_handles:
        if handle != main_page:
            login_page = handle
            break


    # change the control to signin page
    bot.switch_to.window(login_page)
    print("switched")
    time.sleep(3)
    ActionChains(bot).send_keys(Keys.TAB).perform()
    ActionChains(bot).send_keys(Keys.TAB).perform()
    ActionChains(bot).send_keys(Keys.TAB).perform()
    ActionChains(bot).send_keys(Keys.TAB).perform()
    ActionChains(bot).send_keys(Keys.TAB).perform()
    ActionChains(bot).send_keys(Keys.TAB).perform()
    ActionChains(bot).send_keys(Keys.RETURN).perform()
    print("clicked")

    time.sleep(20000)






if __name__=='__main__':
    # for i in range(10):
    #     print(i)
        upload_to_tiktok()