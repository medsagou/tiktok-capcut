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

    # try:
    #     edit_profile =  WebDriverWait(bot, 100).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and .//*[contains(text(), 'Edit profile')]]"))
    # )
    # except Exception as e:
    #     print(e)
    #     print('error, finding the edit profile button')
    #     pass
    # else:
    #     edit_profile.click()
    #     print("EDIT PROFILE FOUND AND CLICKED!")
    #
    # try:
    #     profile_pic_uploder = WebDriverWait(bot, 1000).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))
    #
    # except:
    #     print('error finding the profile pic editor')
    # else:
    #     print("we've find the file uploader button")
    #     # p = os.getcwd()+f'\\render\\{name}.mp4'
    #     p = os.getcwd() + '\\dd.PNG'
    #     print(p)
    #     profile_pic_uploder.send_keys(p)
    #     print("we've send the path to the input")
    #
    # try:
    #     apply_pic = WebDriverWait(bot, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, "//button[text()='{}']".format('Apply'))
    #         )
    #     )
    # except:
    #     print("error appling the pic")
    # else:
    #     apply_pic.click()
    #     print("profile pic applied")
    # try:
    #     bio = WebDriverWait(bot, 10).until(
    #         EC.presence_of_element_located(
    #             (By.CSS_SELECTOR, '[placeholder="Bio"]'))
    #         )
    #
    # except:
    #     print('error, finding the bio input')
    #
    # else:
    #     bio.send_keys('bio text added')
    #     print("bio FOUND AND filed!")
    #
    # try:
    #     submit = WebDriverWait(bot, 10).until(
    #         EC.presence_of_element_located(
    #             (By.CSS_SELECTOR, '[data-e2e="edit-profile-save"]'))
    #     )
    #
    # except:
    #     print('error, finding the edit profile save button')
    #
    # else:
    #     submit.send_keys('bio text added')
    #     print("save EDIT PROFILE FOUND AND CLICKED!")

    print("opening new tab..")
    main_tiktok_page = bot.current_window_handle

    bot.execute_script("window.open('');")

    # Switch to the new tab
    bot.switch_to.window(bot.window_handles[1])
    print("getting capcut site")
    try:
        bot.get('https://www.capcut.com/signup')
    except:
        pass

    main_cacpcut_page = bot.current_window_handle
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
        span_element.click()
        for handle in bot.window_handles:
            if handle != main_tiktok_page and handle != main_cacpcut_page:
                login_page = handle
                break


        # change the control to signin page
        bot.switch_to.window(login_page)
        print("switched to login with tiktok popup...")
        print("finding the Continue button")
        try:
            continue_button =  WebDriverWait(bot, 100).until(
            EC.presence_of_element_located((By.ID, "auth-btn"))
        )
        except Exception as e:
            print(e)
            print('error, finding the Continue button...')
            print("but we will continue!")
            # print(bot.page_source)

        else:
            continue_button.click()
            print("Continue Button FOUND AND CLICKED!")
            time.sleep(2)

        print("Switching to capcut main page")
        bot.switch_to.window(main_cacpcut_page)

    try:
        create_button =  WebDriverWait(bot, 5).until(
        EC.presence_of_element_located((By.ID, "create-bottom"))
    )
    except Exception as e:
        print(e)
        print('error, finding the open capcut button...')
        # print(bot.page_source)

    else:
        create_button.click()
        print("open capcut Button FOUND AND CLICKED!")
        time.sleep(2)

    print("getting the edit page...")
    try:
        bot.get("https://www.capcut.com/editor")
    except Exception as e:
        print(e)
    else:
        print("you are in the edit page")

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



    # try:
    #     WebDriverWait(bot, 100).until(
    #         EC.presence_of_element_located((By.ID, 'canvas-cover')))
    # except Exception as e:
    #     print('we didnt find the canvas cover')
    # else:
    #     print("we did fined the cover canvas")



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
        # utils.check_close_btn(bot)
        # time.sleep(1)
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

    try:
        exporter_first = WebDriverWait(bot, 100).until(
            EC.presence_of_element_located((By.ID, 'export-confirm-button')))
    except:
        print('error finding the EXPORT 2 video button')
    else:
        print("we've find the export 2 video button")
        # utils.check_close_btn(bot)
        # time.sleep(1)
        exporter_first.click()
        print("export 2 button clicked")


    try:
        title_textarea = WebDriverWait(bot, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea")))
    except:
        print("we didnt find the textarea for the title")
    else:
        title_textarea.send_keys("this is a title for the test")
        ActionChains(bot).send_keys(Keys.TAB).perform()
        ActionChains(bot).send_keys(Keys.RETURN).perform()
        # ActionChains(bot).send_keys(Keys.DOWN).perform()
        ActionChains(bot).send_keys(Keys.RETURN).perform()

    try:
        share = WebDriverWait(bot, 1000).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Share']]")))
    except Exception as e:
        print(e, 'we didnt find the share button')
    else:
        share.click()
        print("share button is clicked")

    request = None
    for request in bot.requests:
        print(request.url)
        # print('https://edit-api-sg.capcut.com/lv/v1/share_task/publish_asset_to_third_party_platform')
    time.sleep(300)
    for _ in range(10):  # Adjust the range as needed for your use case
        bot.wait_for_request('publish')
        for req in bot.requests:
            print(req.path)
            if 'publish' in req.path:
                request = req
                print('here', req)
                break
        if request:
            break

    # Check if the request was captured
    if request:
        # Resend the request using the 'requests' library
        response = requests.post(request.url, headers=request.headers, data=request.body)
        response2 = requests.post(request.url, headers=request.headers, data=request.body)

        print(f"First response status code: {response.status_code}")
        print(f"Second response status code: {response2.status_code}")
    else:
        print("The 'publish' request was not captured.")

    print("sleeping")
    time.sleep(2000)

    # Close the browser
    bot.quit()






if __name__=='__main__':
    # for i in range(10):
    #     print(i)
        upload_to_tiktok()