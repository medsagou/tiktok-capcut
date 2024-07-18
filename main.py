import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from playsound import playsound
import files_interaction_utils
import googlesheet
from selenium.common.exceptions import StaleElementReferenceException
# import psutil
# import ray
# import pyautogui

# import logging
# logging.basicConfig(level=logging.DEBUG)


# Huge credits to redianmarku
# https://github.com/redianmarku/tiktok-autouploader

def kill():
    print("clearing...")
    # for proc in psutil.process_iter():
    #     if proc.name() == 'chrome.exe':
    #         proc.kill()
    print("chrome is killed!")

def find_profile(bot):
    try:    
        print('finding the profile')
        profile_element = WebDriverWait(bot, 200).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[data-e2e="nav-profile"]')
            )
        )
    except:
        print('we didnt find the profile')
        try:
            bot.get("https://www.tiktok.com/")
        except:
            print("quiting..")
            bot.quit()
        else:
            try:
                print('finding the profile')
                profile_element = WebDriverWait(bot, 200).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'a[data-e2e="nav-profile"]')
                    )
                )
            except:
                print("quiting..")
                bot.quit()
    else:
        profile_element.click()
        print("PROFILE FOUND AND CLICKED!")


def export_first(bot):
    try:
        # time.sleep(200)
        exporter_first = WebDriverWait(bot, 100).until(
            EC.presence_of_element_located((By.ID, 'export-video-btn')))
        # exporter_first = WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Export"]]')))
    except:
        print('we didn\'t find the EXPORT video button')
    else:
        print("we've find the export video button")
        utils.check_close_btn(bot)
        try:
            exporter_first.click()
        except:
            print("exeption 223")
            utils.check_close_btn
            export_first()
        print("export button clicked")


def upload_to_tiktok(time=0):
    time.sleep(time)
    print("init the bot")
    bot = utils.create_bot() # Might not work in headless mode
    # print("adjusting the window")
    # bot.set_window_size(1920, 1080*2) # Ensure upload button is visible, does not matter if it goes off screen

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
    # try:
    #     # Wait until the text "QR code scanned" appears
    #     WebDriverWait(bot, 30).until(
    #         EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), "QR code scanned")
    #     )
    #     print("The text 'QR code scanned' has appeared!")
    #     # bot.minimize_window()
    # except:
    #     print("The text 'QR code scanned' did not appear within the time limit.")
        
    # try:
    #      WebDriverWait(bot, 1000).until(
    #         EC.presence_of_element_located(
    #             (By.CSS_SELECTOR, '[data-e2e="qr-code"]')
    #         )
    #     )
    # except:
    #     print("qr not found")
    # else:
    #     bot.save_screenshot('screenshot.png')
    #     print("its working")
    
    find_profile(bot=bot)

    try:
        edit_profile =  WebDriverWait(bot, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and .//*[contains(text(), 'Edit profile')]]"))
    )
    except Exception as e:
        print(e)
        print('we didnt find the edit profile button')
        find_profile(bot=bot)
    else:
        edit_profile.click()
        print("EDIT PROFILE FOUND AND CLICKED!")
    
    try:
        profile_pic_uploder = WebDriverWait(bot, 1000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))
    
    except:
        print('we didnt find the profile pic editor')
    else:
        print("we've find the file uploader button")
        # p = os.getcwd()+f'\\render\\{name}.mp4'
        p = os.getcwd() + '\\profile.PNG'
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
        print("we didnt applie the pic")
    else:
        apply_pic.click()
        print("profile pic applied")
    try:
        bio = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[placeholder="Bio"]'))
            )
    
    except:
        print('we ddint found the bio input')
    
    else:
        print("bio :",files_interaction_utils.get_file_content(os.getcwd() + "\\bio.txt"))
        bio.send_keys(files_interaction_utils.get_file_content(os.getcwd() + "\\bio.txt"))
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
        print('we didnt find the video uploader button')
    else:
        print("we've find the video uploader button")
        # p = os.getcwd()+f'\\render\\{name}.mp4'
        video_path = files_interaction_utils.get_first_element_path(os.getcwd() + "\\videos\\")
        new_video_path = files_interaction_utils.add_bracket_to_filename(file_path = video_path)
        print(new_video_path)
        video_uploader.send_keys(new_video_path)
        print("we've send the path to the input")
    bot.switch_to.window(main_tiktok_page)
    
    try:
        submit = WebDriverWait(bot, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-e2e="edit-profile-save"]'))
        )
    
    except:
        print('we didnt find the edit profile save button')
    
    else:
        submit.click()
        print("save EDIT PROFILE FOUND AND CLICKED!")
    profile_link = bot.current_url
    print(profile_link)
    
    bot.switch_to.window(main_cacpcut_page)
    try:
        # Wait until the "Loading..." text is not present in the page
        WebDriverWait(bot, 500).until(
            EC.invisibility_of_element((By.XPATH, "//*[text()='Or drag and drop file here']"))
        )
        print("The 'Or drag and drop file here' text is no longer present on the page.")
    except:
        print("Timed out waiting for 'Or drag and drop file here' text to disappear.")

    

    export_first(bot)

    try:
        TIKTOK = WebDriverWait(bot, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="icon-thirdpart-tiktok"]')))
    except:
        print('we didn\'t find the TIKTOK button')
        export_first(bot)
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
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="icon-thirdpart-tiktok"]')))
        except:
            print('we didn\'t find the TIKTOK button')
            export_first(bot)
        else:
            print("we've find the TIKTOK button")
            # utils.check_close_btn(bot)
            # time.sleep(1)
            TIKTOK.click()
            print("TIKTOK button clicked")
            try:
                TIKTOK = WebDriverWait(bot, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="icon-thirdpart-tiktok"]')))
            except:
                print('we ddint find the TIKTOK button for the second time')



    # time.sleep(200)

    try:
        exporter_second = WebDriverWait(bot, 100).until(
            EC.element_to_be_clickable((By.ID, 'export-confirm-button')))
    except:
        print('we didnt find the EXPORT 2 video button')
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
        title_textarea.send_keys(files_interaction_utils.get_random_line(os.getcwd() + "\\titles.txt") + utils.text_aleatoire())
        ActionChains(bot).send_keys(Keys.TAB).perform()
        ActionChains(bot).send_keys(Keys.RETURN).perform()
        # ActionChains(bot).send_keys(Keys.DOWN).perform()
        ActionChains(bot).send_keys(Keys.RETURN).perform()
        ActionChains(bot).send_keys(Keys.TAB).perform()
        ActionChains(bot).send_keys(Keys.SPACE).perform()

    try:
        share = WebDriverWait(bot, 1000, ignored_exceptions=StaleElementReferenceException).until(
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
        print(f"fifth response status code: {response5.status_code}")
        files_interaction_utils.add_text_to_file(file_path=os.getcwd() + '\\sheet.txt',text = profile_link)
        # gs = googlesheet.GoogleSheet()
        # gs.save(value = profile_link)
        print("removing the file")
        files_interaction_utils.remove_file(new_video_path)
    else:
        print("The 'publish' request was not captured.")

    
    # check if there's any error
        
    try:
    # You can use different locators here. Example: By.XPATH, By.CLASS_NAME, etc.
        body_text = bot.find_element(By.TAG_NAME, 'body').text
        if "Couldn't upload" in body_text:
            print("Text found on the page!")
            playsound(os.getcwd() + "\\notification.wav")
            time.sleep(500)
        else:
            print("Text not found on the page.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        bot.switch_to.window(main_tiktok_page)
        print("closing the browser")
        bot.quit()
        print("browser closed successfuly")
        print("clearing...")
        kill()
        # os.system("taskkill /f /im geckodriver.exe /T")
        # os.system("taskkill /f /im chromedriver.exe /T")
        # os.system("taskkill /f /im IEDriverServer.exe /T")
    except:
        pass




if __name__=='__main__':
    import threading
    print("starting")
    thread1 = threading.Thread(target=upload_to_tiktok)
    thread2 = threading.Thread(target=upload_to_tiktok, args=(5))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    # upload_to_tiktok()
    

