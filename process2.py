from TikTokBot import *
from Chatbot import *
import shutil

api_token = "r8_Cb06Mjr3LNnlc0Cnamkp6N4sW0utmwF4ShBOK"
full_path = r'C:\Users\vesga\Documentos\Victor\Codin_projects\AutoTikTok'

Description_personality = "You reply by the name of Assistant. You will reply directly with an answer. You are a very clickbait person that wants to go viral. You love to add Hashtacks."
search_texts = ['matt walsh LGBQT+', 'Ben Shapiro LGBQT+', 'Piers Morgan LGBQT+']
Description = f'Follow for the truth. Stop this stupiditty from humanity.🥴🥴\n\n#mattwalsh #fyp #foryou #MattWalsh #whatisawoman #woman #transgender #lgbt #factsoverfeelings #fypシ #letstalkaboutit #lgbt #transissues #benshapiro#piersmorgan#gaymarriage#gay #rightwing#politics#encyclopediaconservatism#conservative #conservatives #slander #sugarcrashedit #meme #piersmorgan #pride #lgbtq #debate #samsmith #demilovato #gender #genderidentity #funny #hazardboys'
urls = []

def search_and_download(bot, search_text, num_of_videos=6, scroll=1):
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
    
    # Description_bot = LLMChatBot(api_token)
    bot = tiktokBot(window=True, proxy=False)
    bot.login(interval=0.07)



    print('\033[94m' + 'Empezando rutina de Desacargas' + '\033[0m')
    # for search_text in search_texts:
    #     search_and_download(bot, search_text, num_of_videos=10, scroll=1)
    #     print(f'\nGoing to {search_text}')
    #     bot.updateCSV()
    # #randomize the videos folder
    # with open('videos.txt', 'r') as f:
    #     videos = f.readlines()
    #     random.shuffle(videos)

    print('\033[94m' + 'Saliendo de rutina de Descargas\n' + '\033[0m')



    print('\033[94m' + 'Entrando en rutina de Uploading' + '\033[0m')
    # for video in glob.glob('videos/*.mp4'):
    #     #only upload 5 videos per day
    #     if (bot.numOfUploads > 5 and bot.CheckDate()):
    #         print('We have reached the limit of uploads for today')
    #         break
    #     upload_video(bot, video, Description)
    #     print(f'\nGoing to {video}')
    #     bot.updateCSV()
    print('\033[94m' + 'Saliendo de rutina de Uploading\n' + '\033[0m')
    


    print('\033[94m' + 'Empezando rutina de Following' + '\033[0m')
    for search_text in search_texts:
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