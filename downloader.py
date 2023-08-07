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
import json
from rotating_proxy import get_random_proxy

class tiktokBot():
    def __init__(self, window=True, proxy=False):
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
        self.options.add_argument("--log-level=3")
        
        #remove cookies
        self.options.add_argument("--disable-cookies")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")
        if window == False:
            self.options.add_argument("--headless")

        # #get proxy
        if proxy == True:
            self.proxy = get_random_proxy()
            self.options.add_argument(f'--proxy-server={self.proxy}')

        self.bot = webdriver.Chrome(options=self.options, executable_path=CM().install())
        self.bot.set_window_size(1680, 900)

        self.topic = ''
        self.usernames = []

        self.numOfLikes = 0
        self.numOfFollows = 0
        self.numOfComments = 0
        self.numOfVideos = 0
        self.numOfDownloads = 0

        self.getUserPass()
        #remove the @ and what is after it
        self.csvName = self.email.split('@')[0]
        self.initCSV(f'{self.csvName}.csv')

    def initCSV(self, filename):
        self.filename = filename
        #create csv file if it doesn't exist and write the headers: Date, NumOfLikes, NumOfFollows, NumOfComments, NumOfVideos
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write('Date,NumOfLikes,NumOfFollows,NumOfComments,NumOfVideos,NumOfDownloads\n')
        
        # if there is no date or the date written is not today's date, write the date
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) == 1 or lines[-1].split(',')[0] != time.strftime('%d/%m/%Y'):
                self.updateCSV()

    def updateCSV(self):
        #update the last line of the csv file
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lastLine = lines[-1].split(',')
            lastLine[0] = time.strftime('%d/%m/%Y')
            lastLine[1] = str(self.numOfLikes)
            lastLine[2] = str(self.numOfFollows)
            lastLine[3] = str(self.numOfComments)
            lastLine[4] = str(self.numOfVideos)
            lastLine[5] = str(self.numOfDownloads)
            lines[-1] = ','.join(lastLine)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    def CheckDate(self):
        #return True if the date written in the csv file is today's date
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 1 and lines[-1].split(',')[0] == time.strftime('%d/%m/%Y'):
                return True
            else:
                #update the csv file
                self.updateCSV()
                return False

    def getUserPass(self):
        #read from login.json
        try:
            with open('Utils/login.json') as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    user_info = data[0]  # Access the first dictionary in the list
                    self.email = user_info['username']
                    self.password = user_info['password']
                else:
                    print("Error: 'login.json' does not contain valid user information.")
        except FileNotFoundError:
            print("Error: File 'login.json' not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in 'login.json'.")  


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
            

        for char in self.email:
            self.username.send_keys(char)
            time.sleep(interval)

        self.username.send_keys(Keys.TAB)
        # click tab and write password on the next input
        self.username = self.bot.switch_to.active_element

        # Type the password letter by letter with pauses
        time.sleep(random.randint(1, 4))
        for char in self.password:
            self.username.send_keys(char)
            time.sleep(interval)

        time.sleep(random.randint(3, 7))
        # click enter
        self.username.send_keys(Keys.ENTER)

        try:
            wait = WebDriverWait(self.bot, 5)
            error_message = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@type="error"]//span[@role="status"]')))

            # Verifica si el mensaje de error está presente en la página
            if error_message.is_displayed():
                print("Error:", error_message.text)
                #print in red color
                print('\033[91m' + 'Login failed' + '\033[0m')
                print("Trying again in 10 seconds...\n")
                #sleep for 5 minutes
                time.sleep(10)
                #refresh
                self.refresh()
                #login again
                self.login()
        except:
            #print in green color
            print('\033[92m' + 'Login successfull' + '\033[0m')

    def refresh(self):
        self.bot.refresh()

    def search(self, topic):
        print('Searching for', topic)
        self.topic = topic
        #seqrch by name q = self.bot.find_element_by_name('q'), click and write topic and hit enter
        try:
            self.searchBTN = self.bot.find_element_by_name('q')
            time.sleep(0.5)
            self.searchBTN.click()
            self.searchBTN.send_keys(topic)
            self.searchBTN.send_keys(Keys.ENTER)
        except:
            print('\033[91m' + 'Error searching for ' + topic + '\033[0m')
            time.sleep(5)

    def scroll(self, scroll_times=10):
        print('Scrolling...')
        for i in range(scroll_times):
            self.bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.5)

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
        print('Not filtered videos:', len(self.urls))
        self.urls = self._filter_videos()
        print('Filtered videos: ', len(self.urls))
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
                self.numOfDownloads += 1


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
        ActionChains(self.bot).move_to_element(upload_button).send_keys(Keys.TAB * 11).send_keys(Keys.ENTER).perform()

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
        time.sleep(1)
        ActionChains(self.bot).move_to_element(current).send_keys(Keys.TAB * 5).perform()
        time.sleep(1)
        # Paste the description into the label box
        self.bot.switch_to.active_element

        time.sleep(1)
        #write the description
        pyperclip.copy(description)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # pyautogui.write(description)
        print('Description added!')

        ############################## Uplad video ####################################
        #11 tabs to get to the post button from the description box
        ActionChains(self.bot).send_keys(Keys.TAB * 11).perform()
        time.sleep(1)
        print('Tabbed to post button')
        #Get the current selected field and click enter
        boton_post = self.bot.switch_to.active_element
        print(f'Current selected field: {boton_post}')
        #click enter
        ActionChains(self.bot).move_to_element(boton_post).send_keys(Keys.ENTER).perform()

        print('Video uploaded!')
        self.numOfVideos += 1
        time.sleep(10)


        ############################## Closing tab ####################################
        print('Closing tab...')
        #add a new tab and close the previous one
        self.bot.execute_script("window.open('');")
        self.bot.switch_to.window(self.bot.window_handles[0])
        self.bot.close()
        self.bot.switch_to.window(self.bot.window_handles[0])

        time.sleep(2)
        
    
    def like_comments(self, url, scroll_times=10):
        
        self.bot.get(url)
        self.likeVideo()
        
        try:
            
            WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@data-e2e='comment-like-count']")))
            self.scroll(scroll_times)

            # Encuentra todos los elementos que representan los contadores de "me gusta" de los comentarios
            like_counters = self.bot.find_elements_by_xpath("//span[@data-e2e='comment-like-count']")
            print(f'Cantidad de comentarios encontrados: {len(like_counters)}')
            self.getUsersFromComments()

            print('Empezando a dar me gusta a los comentarios...')
            for counter in like_counters:
                try:
                    #dar like a los comentarios
                    self.bot.execute_script("arguments[0].click();", counter)
                    self.numOfLikes += 1
                    time.sleep(0.2)
                except Exception as e:
                    # print in red color
                    print('\033[91m' + "Error al dar 'me gusta' en los comentarios." + '\033[0m')
                    continue

            # print in green color
            print('\033[92m' + "Me gusta en los comentarios realizados correctamente." + '\033[0m')
        except Exception as e:
            # print in red color
            print('\033[91m' + "Error al dar 'me gusta' en los comentarios." + '\033[0m')

    def getUsersFromComments(self):
        #get all the users that are on data-e2e="comment-username-1"
        self.usernames = []
        # user_elements = self.bot.find_elements_by_css_selector('[data-e2e="comment-username-1"]')
        # usernames = [element.text for element in user_elements]
        # user elements are all the hrefs that are on the data-e2e="search-comment-container" div
        user_elements = self.bot.find_elements_by_css_selector('[data-e2e="search-comment-container"] a')
        self.usernames = [element.get_attribute('href').split('/')[3] for element in user_elements]
        #remove repeated usernames
        self.usernames = list(dict.fromkeys(self.usernames))
        print(f'Cantidad de usuarios entonctrados: {len(self.usernames)}')

    def followAccounts(self, url=None):
        print('Following accounts...')
        #empty self.usernames
        if url:
            self.bot.get(url)
            time.sleep(5)
        for username in self.usernames:
            try:
                #go to https://www.tiktok.com/ + username
                self.goTo(f'https://www.tiktok.com/{username}')
                time.sleep(0.1)
                #click on follow
                follow_user = self.bot.find_elements_by_css_selector('[data-e2e="follow-button"]')
                follow_user[0].click()
                time.sleep(1.5)
                print('\033[92m' + f'Siguiendo a {username}' + '\033[0m')
                self.numOfFollows += 1
            except Exception as e:
                print('\033[91m' + f"Error al seguir a {username}." + '\033[0m')
                continue
        # print('\033[92m' + "Usuarios seguidos correctamente." + '\033[0m')



    def likeVideo(self, url=None):
        if url:
            self.bot.get(url)
            time.sleep(5)

        try:
            like_button = self.bot.find_element_by_css_selector('.tiktok-riabsu-DivVideoContainer')
            # Realizar el doble clic para dar like al video
            actions = ActionChains(self.bot)
            actions.double_click(like_button).perform()
            # print in green color
            print('\033[92m' + "Me gusta en el video realizado correctamente." + '\033[0m')
            self.numOfLikes += 1
        except Exception as e:
            # print in red color
            print('\033[91m' + "Error al dar 'me gusta' en el video." + '\033[0m')

    def close(self):
        self.bot.quit()


# bot = tiktokBot()
# bot.login()
# time.sleep(5)
# bot.search('magic the gathering')
# bot.scroll(15)
# time.sleep(2)
# videos = bot.GetURLs()
# while videos is None:
#     bot.refresh()
#     videos = bot.GetURLs()

# for video in videos:
#     print(f'\nGoing to {video}')
#     bot.like_comments(video, 20)
#     bot.followAccounts(video)