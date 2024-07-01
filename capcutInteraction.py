import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui


bot = utils.create_bot() # Might not work in headless mode
print("adjusting the window")
bot.set_window_size(1920, 1080*2) # Ensure upload button is visible, does not matter if it goes off screen

# Fetch main page to load cookies, sometimes infinte loads, except and pass to keep going
print("getting the site")
while True:
    try:
        bot.get('https://www.capcut.com/editor')
    except Exception as e:
        print(e)
        print("refreshing...")
    else:
        print("site is here")
        time.sleep(2)
        break

try:
    # Wait until the "Loading..." text is not present in the page
    WebDriverWait(bot, 100).until(
        EC.invisibility_of_element((By.XPATH, "//*[text()='Loading...']"))
    )
    print("The 'Loading...' text is no longer present on the page.")
except:
    print("Timed out waiting for 'Loading...' text to disappear.")


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
    print('sleeping')

utils.check_close_btn(bot)

try:
    # Wait until the "Loading..." text is not present in the page
    WebDriverWait(bot, 100).until(
        EC.invisibility_of_element((By.XPATH, "//*[text()='Or drag and drop file here']"))
    )
    print("The 'Or drag and drop file here' text is no longer present on the page.")
except:
    print("Timed out waiting for 'Or drag and drop file here' text to disappear.")

utils.check_close_btn(bot)
try:
    exporter_first = WebDriverWait(bot, 100).until(
        EC.presence_of_element_located((By.ID, 'export-video-btn')))
except:
    print('error finding the EXPORT video button')
else:
    print("we've find the export video button")
    utils.check_close_btn(bot)
    time.sleep(1)
    exporter_first.click()
    print("export button clicked")
    time.sleep(20000)