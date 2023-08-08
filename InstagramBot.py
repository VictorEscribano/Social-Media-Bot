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
from TikTokBot import tiktokBot

class instagramBot(tiktokBot):
    #inherit from tiktokBot the getUserPass function

    def __init__(self, window=True, proxy=False):
        super().__init__(window, proxy)
        self.url = 'https://www.instagram.com/'
        self.login_url = 'https://www.instagram.com/accounts/login/'
        
        self.getUserPass(filename='InstagramUserPass.json')
    

    def UploadVideo(self):
        try:
            #click on the class x1n2onr6
            WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x1n2onr6'))).click()
            print("Clicked on 'Nueva publicación' button.")
            
        except Exception as e:
            print("Error:", e)
    

bot = instagramBot(window=True, proxy=False)
time.sleep(2)
bot.login(interval=0.07, url=bot.login_url)
time.sleep(2)
bot.UploadVideo()
time.sleep(10)
bot.close() 
