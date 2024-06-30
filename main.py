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
    while True:
        try:
            bot.get('https://www.tiktok.com/login/qrcode')
        except Exception as e:
            print(e)
            print("refreshing...")
        else:
            break
    time.sleep(4)
    print('finding the profile')
    try:
        profile_element = WebDriverWait(bot, 1000).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[data-e2e="nav-profile"]')
            )
        )
    except:
        print('error, finding the profile')
        pass
    else:
        profile_element.click()
        print("PROFILE FOUND AND CLICKED!")

    try:
        edit_profile =  WebDriverWait(bot, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and .//*[contains(text(), 'Edit profile')]]"))
    )
    except Exception as e:
        print(e)
        print('error, finding the edit profile button')
        pass
    else:
        edit_profile.click()
        print("EDIT PROFILE FOUND AND CLICKED!")

    try:
        profile_pic_uploder = WebDriverWait(bot, 1000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))

    except:
        print('error finding the profile pic editor')
    else:
        print("we've find the file uploader button")
        # p = os.getcwd()+f'\\render\\{name}.mp4'
        p = os.getcwd() + '\\dd.PNG'
        print(p)
        profile_pic_uploder.send_keys(p)
        print("we've send the path to the input")

    try:
        apply_pic = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='{}']".format('Apply'))
            )
        )
    except:
        print("error appling the pic")
    else:
        apply_pic.click()
        print("profile pic applied")
    try:
        bio = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[placeholder="Bio"]'))
            )

    except:
        print('error, finding the bio input')

    else:
        bio.send_keys('bio text added')
        print("bio FOUND AND filed!")

    print('sleeping')
    time.sleep(10000)
    try:
        submit = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-e2e="edit-profile-save"]'))
        )

    except:
        print('error, finding the edit profile save button')

    else:
        submit.send_keys('bio text added')
        print("save EDIT PROFILE FOUND AND CLICKED!")

    print('sleeping')
    time.sleep(10000)

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