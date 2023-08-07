from downloader import *
from Chatbot import *
import shutil

api_token = "r8_Cb06Mjr3LNnlc0Cnamkp6N4sW0utmwF4ShBOK"
full_path = r'C:\Users\vesga\Documentos\Victor\Codin_projects\AutoTikTok'

Description_personality = "You reply by the name of Assistant. You will reply directly with an answer. You are a very clickbait person that wants to go viral. You love to add Hashtacks."
search_text = 'aliens ufo UAV US government'
Description = f'Like and subscribe for more videos! {search_text}'

def search_and_download(bot, search_text, scroll=8):
    time.sleep(5)
    bot.search(search_text)
    time.sleep(3)
    bot.scroll(scroll)

    urls = bot.GetURLs()
    print(urls)
    time.sleep(1)
    for i, url in enumerate(urls):
        print(f'Downloading video {i} of {len(urls)}')
        bot.download_video(url, i)
        time.sleep(10)
    time.sleep(5)
    pass

def upload_video(bot, video, Description):
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

if __name__ == "__main__":
    
    Description_bot = LLMChatBot(api_token)
    bot = tiktokBot(window=True, proxy=False)

    bot.login(interval=0.07)
    search_and_download(bot, search_text, scroll=2)

    print('Entering upload loop...')
    for video in glob.glob('videos/*.mp4'):
        
        upload_video(bot, video, Description)

        