from downloader import *
from Chatbot import *


if __name__ == "__main__":
    api_token = "r8_Cb06Mjr3LNnlc0Cnamkp6N4sW0utmwF4ShBOK"
    Description_personality = "You reply by the name of Assistant. You will reply directly with an answer. You are a very clickbait person that wants to go viral."
    

    Description_bot = LLMChatBot(api_token)
    bot = tiktokBot(window=True)
    bot.login(interval=0.07)
    search_text = '#viral'
    

    # time.sleep(5)
    # bot.search(search_text)
    # time.sleep(3)
    # bot.scroll(8)

    # urls = bot.GetURLs()
    # print(urls)
    # time.sleep(1)
    # for i, url in enumerate(urls):
    #     print(f'Downloading video {i} of {len(urls)}')
    #     bot.download_video(url, i)
    #     time.sleep(10)
    # time.sleep(5)

    print('Entering upload loop...')
    time.sleep(6)
    full_path = r'C:\Users\vesga\Documentos\Victor\Codin_projects\AutoTikTok'
    for video in glob.glob('videos/*.mp4'):
        Description_prompt_input = f"Reply with a very realistic Tik-Tok video description and a lot of hashtacks about this video topic: {video}. It needs to go viral. Assistant:"
        Description = Description_bot.generate_response(Description_personality, 
                                                        Description_prompt_input, 
                                                        temperature=0.5, 
                                                        top_p=0.6, 
                                                        max_length=160, 
                                                        repetition_penalty=1)
        
        time.sleep(5)
        if Description == None:
            print('Error generating description')
            Description = 'Like and subscribe for more videos! '
        else:
            print(f'Description: {Description}')

        try:
            bot.upload2TikTok(f'{full_path}\{video}', f'{Description} ')
        except:
            print('Error uploading video')
            bot.goToNewTab()
            continue

        time.sleep(1)
        #move the video to the Used_videos folder
        shutil.move(video, 'Used_videos')
        time.sleep(1)