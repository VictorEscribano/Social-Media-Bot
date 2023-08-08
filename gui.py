import streamlit as st
import time
import subprocess
from TikTokBot import *
from Chatbot import *
import shutil


def download_routine(bot, search_text, num_of_videos=4, scroll=1):
    print('\033[94m' + 'Empezando rutina de Desacargas' + '\033[0m')
    st.write("Running Download Routine")
    global urls
    time.sleep(8)
    bot.search(search_text)
    time.sleep(5)
    bot.scroll(scroll)

    urls = bot.GetURLs()
    while len(urls) < num_of_videos:
        bot.scroll(1)
        urls = bot.GetURLs()
        time.sleep(1)
    # get only the number of videos we want
    urls = urls[:num_of_videos]
    print(f'Found {len(urls)} videos')
    time.sleep(1)
    for i, url in enumerate(urls):
        print(f'Downloading video {i} of {len(urls)}')
        bot.download_video(url, i)
        time.sleep(10)
    time.sleep(5)
    print('\033[94m' + 'Saliendo de rutina de Descargas\n' + '\033[0m')

def upload_routine(bot, video, Description, full_path):
    print('\033[94m' + 'Entrando en rutina de Uploading' + '\033[0m')
    st.write("Running Upload Routine")
    if Description == None:
        print('Error generating description')
        Description = 'Like and subscribe for more videos! '
    else:
        print(f'Description: {Description}')

    try:
        bot.upload2TikTok(f'{full_path}\{video}', f'{Description} ')
        time.sleep(1)
        shutil.move(video, 'Used_videos')
        time.sleep(1)
    except Exception as e:
        print(f'Error uploading video: {e}')
        bot.goToNewTab()
    print('\033[94m' + 'Saliendo de rutina de Uploading\n' + '\033[0m')

def like_follow_routine(bot, search_text):
    print('\033[94m' + 'Empezando rutina de Following' + '\033[0m')
    st.write("Running Like and Following Routine")
    bot.goTo('https://www.tiktok.com/')
    time.sleep(2)
    bot.search(search_text)
    time.sleep(5)
    bot.scroll(1)
    urls = bot.GetURLs()
    time.sleep(1)
    for url in urls:
        print(f'\nGoing to {url}')
        # check if we uploaded more than 200 videos today
        if (bot.numOfLikes > 200 and bot.CheckDate()):
            print('We have reached the limit of likes for today')
        else:
            bot.like_comments(url, 4)
        bot.followAccounts(url)
        bot.updateCSV()
    print('\033[94m' + 'Saliendo de la rutina de Following' + '\033[0m')

def main():
    st.title("TikTok Automation App")

    # User and Password UI
    st.header("Login and Password")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Download Routine UI
    st.header("Download Routine")
    search_topics = st.text_input("Enter search topics (comma-separated)", "FunnyMemes,DankMemes")
    num_videos = st.number_input("Number of videos to download", min_value=1, value=5)
    download_enabled = st.checkbox("Enable Download Routine", key="download_enabled")

    # Upload Routine UI
    st.header("Upload Routine")
    videos_folder = st.text_input("Paste the path where videos will be saved", "/path/to/videos")
    num_uploads = st.number_input("Number of uploads to do", min_value=1, value=3)
    description = st.text_area("Video Description")
    upload_enabled = st.checkbox("Enable Upload Routine", key="upload_enabled")

    # Like and Following Routine UI
    st.header("Like and Following Routine")
    like_follow_enabled = st.checkbox("Enable Like and Following Routine", key="like_follow_enabled")

    if st.button("Start"):
        bot = tiktokBot(window=True, proxy=False)

        if username: bot.email = username
        if password: bot.password = password
        bot.login(interval=0.07)
        
        console = st.empty()
        console.text("Starting routines...")

        if download_enabled:
            for search_text in search_topics.split(","):
                download_routine(bot, search_text, num_of_videos=num_videos, scroll=1)
                console.text(f'Going to {search_text}')
        
        if upload_enabled:
            video_files = os.listdir(videos_folder)
            for video in video_files:
                if (bot.numOfUploads > num_uploads and bot.CheckDate()):
                    console.text('We have reached the limit of uploads for today')
                    break
                upload_routine(bot, video, description, videos_folder)
                console.text(f'Uploading video {video}')
                shutil.move(os.path.join(videos_folder, video), 'Used_videos')
                time.sleep(1)

        if like_follow_enabled:
            for search_text in search_topics.split(","):
                like_follow_routine(bot, search_text)

        console.text("Routines completed.")

if __name__ == "__main__":
    main()
