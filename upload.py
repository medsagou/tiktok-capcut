import time,os,utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils import config

# Huge credits to redianmarku
# https://github.com/redianmarku/tiktok-autouploader

def upload_to_tiktok(name,title):
    print("init the bot")
    bot = utils.create_bot(headless=False) # Might not work in headless mode
    print("adjusting the window")
    bot.set_window_size(1920, 1080*2) # Ensure upload button is visible, does not matter if it goes off screen

    # Fetch main page to load cookies, sometimes infinte loads, except and pass to keep going
    print("getting the site")
    try:
        bot.get('https://www.tiktok.com/')
    except:
        pass
    print("writing the cookies")
    for cookie in config['tiktok_cookies'].split('; '):
        data = cookie.split('=')
        bot.add_cookie({'name':data[0],'value':data[1]})
    print("getting the upload site")
    try:
        bot.get('https://www.tiktok.com/upload')
    except:
        pass


    # bot.switch_to.frame(bot.find_element(By.TAG_NAME,"iframe"))

    # Wait for 1 second
    time.sleep(1)

    # Upload video
    file_uploader = WebDriverWait(bot, 1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[type="file"]')))
    print("we've find the file uploader button")
    # p = os.getcwd()+f'\\render\\{name}.mp4'
    p = os.getcwd()+f'\\{name}.mp4'
    print(p)
    file_uploader.send_keys(p)
    print("we've send the path to the input")

    # Focus caption element
    caption = WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')))
    ActionChains(bot).click(caption).perform()

    # Input title & tags
    # print('📝 Writing title & tags...')
    print("title and tags..")
    if len(title) < 70:
        try:
            ActionChains(bot).send_keys(title+" ").perform()
            tags = ["reddit","meme","askreddit","story","storytime","fyp"]
            for tag in tags:
                ActionChains(bot).send_keys("#"+tag).perform()
                # WebDriverWait(bot, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mentionSuggestions')))
                time.sleep(3)
                ActionChains(bot).send_keys(Keys.RETURN).perform()
                time.sleep(0.05)
        except:
            pass

    try:
        print("⏱ Waiting to post...")
	# print("posting...")
        # Scroll to bottom to make sure post button is visible
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for 'Post' button to be active, then click
        post = WebDriverWait(bot, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div/div/div[4]/div/div[2]/div[9]/button[1]')))
        print('we did find the post button')
        ActionChains(bot).move_to_element(post).perform()
        ActionChains(bot).click(post).perform()
        print("posting button clicked")

        # Wait for confirmation, then exit
        try:
            WebDriverWait(bot, 100).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),  # Search within the entire body of the page
                    'Your video has been uploaded'
                )
            )
        except Exception as e:
            print("Error while uploading the video", e)
        else:
            print("the video uploaded succ")
        time.sleep(0.2)
        bot.close()
        return True
    except:
        bot.close()
        return False

if __name__=='__main__':
    upload_to_tiktok(name="123", title='123')