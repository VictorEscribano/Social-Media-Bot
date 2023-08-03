import glob
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pyautogui
import os
import pyperclip
import platform
import random
import subprocess

class tiktokBot():
    def __init__(self, window=True):
        self.options = Options()
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--profile-directory=Default")
        self.options.add_argument("--incognito")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-plugins-discovery")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--disable-popup-blocking")

        #remove cookies
        self.options.add_argument("--disable-cookies")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        if window == False:
            self.options.add_argument("--headless")

        self.bot = webdriver.Chrome(options=self.options, executable_path=CM().install())
        self.bot.set_window_size(1680, 900)

        self.topic = ''

    def goTo(self, url):
        self.bot.get(url)


    def goToNewTab(self, url=None):
        #new tab
        self.bot.execute_script("window.open('');")
        #switch to new tab
        self.bot.switch_to.window(self.bot.window_handles[1])
        #go to url
        if url != None:
            self.goTo(url)


    def login(self, url='https://www.tiktok.com/login/phone-or-email/email', interval=0.2):
        #goto url
        self.goTo(url)

        # find element by name: username, click it and write victorescribanogarcia@gmail.com
        time.sleep(random.randint(1, 4))
        self.username = self.bot.find_element_by_name('username')
        self.username.click()

        # Type the email address letter by letter with pauses
        email = 'victorescribanogarcia@gmail.com'
        # email = 'bakuvic@hotmail.com'
        password = 'Victor123*'                         

        
        for char in email:
            self.username.send_keys(char)
            time.sleep(interval)

        self.username.send_keys(Keys.TAB)
        # click tab and write password on the next input
        self.username = self.bot.switch_to.active_element

        # Type the password letter by letter with pauses
        time.sleep(random.randint(1, 4))
        for char in password:
            self.username.send_keys(char)
            time.sleep(interval)

        time.sleep(random.randint(5, 30))
        # click enter
        self.username.send_keys(Keys.ENTER)

        try:
            wait = WebDriverWait(self.bot, 3)
            error_message = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@type="error"]//span[@role="status"]')))

            # Verifica si el mensaje de error está presente en la página
            if error_message.is_displayed():
                print("Error:", error_message.text)
                print("Login failed")
                print("Trying again in 5 minutes")
                #sleep for 5 minutes
                time.sleep(10)
                #refresh
                self.refresh()
                #login again
                self.login()
        except:
            print('Login successfull')

    def refresh(self):
        self.bot.refresh()

    def search(self, topic):
        print('Searching for', topic)
        self.topic = topic
        #seqrch by name q = self.bot.find_element_by_name('q'), click and write topic and hit enter
        self.search = self.bot.find_element_by_name('q')
        self.search.click()
        self.search.send_keys(topic)
        self.search.send_keys(Keys.ENTER)

    def scroll(self, scroll_times=10):
        print('Scrolling...')
        for i in range(scroll_times):
            self.bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)

    def _filter_videos(self):
        # Create a new list to store the filtered URLs
        filtered_urls = []
        
        # Check if the word 'video' is in the URL, and if yes, add it to the filtered list
        for url in self.urls:
            if '/video/' in url:
                filtered_urls.append(url)
                
        # Assign the filtered URLs back to self.urls
        self.urls = filtered_urls
        
        return self.urls
    
    def GetURLs(self):
        self.urls = []
        # get all the classes that starts with tiktok- and get the href if it exists
        videos = self.bot.find_elements_by_xpath("//div[starts-with(@class, 'tiktok-')]//a[@href]")
        self.urls = [video.get_attribute('href') for video in videos ]
        self.urls = self._filter_videos()
        print('Found', len(self.urls), 'videos')
        return self.urls

    def download_video(self, url, id):
        cookies = {
            '_gid': 'GA1.2.930354431.1690998059',
            '_gat_UA-3524196-6': '1',
            '_ga': 'GA1.2.294704159.1690998059',
            '_ga_ZSF3D6YSLC': 'GS1.1.1690998058.1.0.1690998112.0.0.0',
        }

        headers = {
            'authority': 'ssstik.io',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_gid=GA1.2.930354431.1690998059; _gat_UA-3524196-6=1; _ga=GA1.2.294704159.1690998059; _ga_ZSF3D6YSLC=GS1.1.1690998058.1.0.1690998112.0.0.0',
            'hx-current-url': 'https://ssstik.io/en',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'referer': 'https://ssstik.io/en',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        }

        params = {
            'url': 'dl',
        }

        data = {
            'id': url,
            'locale': 'en',
            'tt': 'RHc5ZjRk',
        }

        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
        downloadSoup = BeautifulSoup(response.text, 'html.parser')
        downloadURL = downloadSoup.a['href']

        mp4file = urlopen(downloadURL)
        with open(f'videos/{self.topic}_{id}.mp4', 'wb') as output:
            while True:
                buffer = mp4file.read(4096)
                if not buffer:
                    break
                output.write(buffer)

    def copy_to_clipboard(text):
        if platform.system() == "Windows":
            # Windows: use 'clip' command
            subprocess.run("echo " + text.strip() + "| clip", shell=True)
        elif platform.system() == "Darwin":
            # macOS: use 'pbcopy' command
            subprocess.run("echo " + text.strip() + "| pbcopy", shell=True)
        else:
            # Linux: use 'xclip' command
            subprocess.run("echo " + text.strip() + "| xclip -selection clipboard", shell=True)


    def upload2TikTok(self, video, description):
        #render the headless browser
        self.bot.set_window_size(1920, 1080)

        ############################## Opening preUploading Page ##############################
        print('Entering PreUploading page...')
        #https://www.tiktok.com/upload?lang=en go here
        self.goTo('https://www.tiktok.com/upload?lang=en')

        ############################## Select video ########################################  
        time.sleep(10)
        print(f'Selecting video {video}...')
        upload_button = self.bot.switch_to.active_element
        ActionChains(self.bot).move_to_element(upload_button).send_keys(Keys.TAB * 8).send_keys(Keys.ENTER).perform()

        ############################## Selecting video from file explorer ####################
        # copy the video path to the clipboard
        pyperclip.copy(video)
        #another method to copy the video path to the clipboard
        
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        print(f'Video selected! {video}')
        time.sleep(1)

        ############################## Entering Uploading page ####################################
        print('Entering Uploading page...')
        #click on aria-label="Caption"
        #tab 6 times after waiting 15 secs
        
        #TODO no esperar 15 sino buscar un indicativo que diga que el video ya se subio
        time.sleep(15)
        ############################## Adding description ####################################
        # label_box get current selected field use action chains to tab 6 times from the current selected field
        current = self.bot.switch_to.active_element
        ActionChains(self.bot).move_to_element(current).send_keys(Keys.TAB * 5).perform()
        # Paste the description into the label box
        self.bot.switch_to.active_element
        #write the description
        pyperclip.copy(description)
        pyautogui.hotkey('ctrl', 'v')
        # pyautogui.write(description)
        print('Description added!')

        ############################## Uplad video ####################################
        #11 tabs to get to the post button from the description box
        ActionChains(self.bot).send_keys(Keys.TAB * 10).perform()
        print('Tabbed to post button')
        #Get the current selected field and click enter
        boton_post = self.bot.switch_to.active_element
        print(f'Current selected field: {boton_post}')
        #click enter
        ActionChains(self.bot).move_to_element(boton_post).send_keys(Keys.ENTER).perform()
        print('Video uploaded!')
        time.sleep(5)

        #add a new tab and close the previous one
        self.bot.execute_script("window.open('');")
        self.bot.switch_to.window(self.bot.window_handles[0])
        self.bot.close()
        self.bot.switch_to.window(self.bot.window_handles[0])

        time.sleep(2)
        
    
    def upload2Instagram(self, video, description):
        pass

    def upload2Facebook(self, video, description):
        pass

    def upload2Youtube(self, video, description):
        pass

    def close(self):
        self.bot.quit()
