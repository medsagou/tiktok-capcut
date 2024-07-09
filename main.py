import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
# import pyautogui


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
    try:
        # Wait until the text "QR code scanned" appears
        WebDriverWait(bot, 30).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "QR code scanned")
        )
        print("The text 'QR code scanned' has appeared!")
        # bot.minimize_window()
    except:
        print("The text 'QR code scanned' did not appear within the time limit.")
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
        bio.send_keys('bio text added.')
        print("bio FOUND AND filed!")

    print("opening new tab...")
    main_tiktok_page = bot.current_window_handle

    bot.execute_script("window.open('https://www.capcut.com/editor');")

    # Switch to the new tab
    bot.switch_to.window(bot.window_handles[1])
    # print("getting capcut site")
    # try:
    #     bot.get('https://www.capcut.com/signup')
    # except:
    #     pass

    main_cacpcut_page = bot.current_window_handle
    utils.handle_login_element(bot, main_tiktok_page, main_cacpcut_page)
            
    
    try:
        # Wait until the "Loading..." text is not present in the page
        WebDriverWait(bot, 500).until(
            EC.invisibility_of_element((By.XPATH, "//*[text()='Loading...']"))
        )
        print("The 'Loading...' text is no longer present on the page.")
    except:
        print("Timed out waiting for 'Loading...' text to disappear.")

    try:
        # Wait until the button with a child containing the text 'Upload' is present
        WebDriverWait(bot, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[.//text()='Upload']"))
        )

        # Do something with the button
        print("Button found: ")

        # Example action: click the button
        # button.click()

    except Exception as e:
        print(f"we didn't find the upload")

    utils.check_close_btn(bot)

    try:
        video_uploader = WebDriverWait(bot, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))
    except:
        print('error finding the video uploader button')
    else:
        print("we've find the video uploader button")
        # p = os.getcwd()+f'\\render\\{name}.mp4'
        p = os.getcwd() + '\\123.mp4'
        print(p)
        video_uploader.send_keys(p)
        print("we've send the path to the input")
    bot.switch_to.window(main_tiktok_page)
    
    try:
        submit = WebDriverWait(bot, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-e2e="edit-profile-save"]'))
        )
    
    except:
        print('error, finding the edit profile save button')
    
    else:
        submit.click()
        print("save EDIT PROFILE FOUND AND CLICKED!")
    
    bot.switch_to.window(main_cacpcut_page)
    try:
        # Wait until the "Loading..." text is not present in the page
        WebDriverWait(bot, 500).until(
            EC.invisibility_of_element((By.XPATH, "//*[text()='Or drag and drop file here']"))
        )
        print("The 'Or drag and drop file here' text is no longer present on the page.")
    except:
        print("Timed out waiting for 'Or drag and drop file here' text to disappear.")

    try:
        exporter_first = WebDriverWait(bot, 100).until(
            EC.presence_of_element_located((By.ID, 'export-video-btn')))
    except:
        print('error finding the EXPORT video button')
    else:
        print("we've find the export video button")
        utils.check_close_btn(bot)
        exporter_first.click()
        print("export button clicked")

    

    try:
        TIKTOK = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[name="icon-thirdpart-tiktok"]')))
    except:
        print('error finding the TIKTOK button')
    else:
        print("we've find the TIKTOK button")
        # utils.check_close_btn(bot)
        # time.sleep(1)
        TIKTOK.click()
        print("TIKTOK button clicked")

    print(len(bot.window_handles))

    if len(bot.window_handles) > 2:
        utils.handle_auth_tiktok(bot, main_tiktok_page, main_cacpcut_page)
        try:
            TIKTOK = WebDriverWait(bot, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[name="icon-thirdpart-tiktok"]')))
        except:
            print('error finding the TIKTOK button')
        else:
            print("we've find the TIKTOK button")
            # utils.check_close_btn(bot)
            # time.sleep(1)
            TIKTOK.click()
            print("TIKTOK button clicked")



    # time.sleep(200)

    try:
        exporter_second = WebDriverWait(bot, 100).until(
            EC.element_to_be_clickable((By.ID, 'export-confirm-button')))
    except:
        print('error finding the EXPORT 2 video button')
    else:
        print("we've find the export 2 video button")
        # utils.check_close_btn(bot)
        # time.sleep(1)
        exporter_second.click()
        print("export 2 button clicked")

    try:
        title_textarea = WebDriverWait(bot, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea")))
    except:
        print("we didnt find the textarea for the title")
    else:
        title_textarea.send_keys("this is a title for the test" + utils.text_aleatoire())
        ActionChains(bot).send_keys(Keys.TAB).perform()
        ActionChains(bot).send_keys(Keys.RETURN).perform()
        # ActionChains(bot).send_keys(Keys.DOWN).perform()
        ActionChains(bot).send_keys(Keys.RETURN).perform()
        ActionChains(bot).send_keys(Keys.TAB).perform()
        ActionChains(bot).send_keys(Keys.SPACE).perform()

    try:
        share = WebDriverWait(bot, 1000).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Share']]")))
    except Exception as e:
        print(e, 'we didnt find the share button')
    else:
        share.click()
        print("share button is clicked")
    # -------------------------------------------------------------------------------------
    # time.sleep(10)
    request = None
    print("searching for the request")
    request = utils.get_request(bot)
    if request:
        print("requesting now")
        # Resend the request using the 'requests' library
        response = requests.post(request.url, headers=request.headers, data=request.body)
        response2 = requests.post(request.url, headers=request.headers, data=request.body)
        response3 = requests.post(request.url, headers=request.headers, data=request.body)
        response4 = requests.post(request.url, headers=request.headers, data=request.body)
        response5 = requests.post(request.url, headers=request.headers, data=request.body)
        print(f"First response status code: {response.status_code}")
        print(f"Second response status code: {response2.status_code}")
        print(f"third response status code: {response3.status_code}")
        print(f"fourth response status code: {response4.status_code}")
        print(f"fourth response status code: {response5.status_code}")
    else:
        print("The 'publish' request was not captured.")

    # print("sleeping")
    # time.sleep(2000)

    # Close the browser
    print("closing the browser")
    bot.quit()






if __name__=='__main__':
    # for i in range(10):
    #     print(i)
        upload_to_tiktok()