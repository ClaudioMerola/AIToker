import config
import requests
import cv2
import datetime
from utils import *

# Function to trigger the initial phase, which processes the news article and creates a video.
def func_editor(content, source: str):

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Entering editor room...")
    var_link = content.link
    var_title = content.title
    try:

        if (source == 'NYTimes'):
            print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Saving NYTimes article screenshot...")
            var_url = content.media_content[0]['url']
            var_request = requests.get(var_url)
            open((config.PATH_TO_SCREENSHOT+'NewsScreenShot.png'), 'wb').write(var_request.content)
            print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Editing NYTimes article screenshot...")
            var_img_core = cv2.imread(config.PATH_TO_SCREENSHOT+"NewsScreenShot.png")
            var_cropped_img = var_img_core[100:(var_img_core.shape[0]-100), 0:var_img_core.shape[1]]
            # Scaling the image to fit the video
            var_scale = 540 / var_cropped_img.shape[0]
            var_img_resized = cv2.resize(var_cropped_img, None, fx = var_scale, fy = var_scale,interpolation=cv2.INTER_AREA)
            height_cutoff = 400
            var_img_resized = var_img_resized[:height_cutoff, :]
            #var_img_resized = cv2.resize(var_img_core, (920, 400),interpolation=cv2.INTER_AREA)
            cv2.imwrite((config.PATH_TO_SCREENSHOT+"NewsScreenShot.png"), var_img_resized)
            
        else:
            # ScreenShot
            func_take_sitescreenshot(var_link, source)

        var_ai_prompt = (config.AI_PROMPT+var_link)

        if (config.AI_TOOL == 'openai'):
            var_ai_response = func_openai(var_ai_prompt,var_link)
        else:
            var_ai_response = func_azureopenai(var_ai_prompt,var_link)

        var_temp_mp3 = func_core_audiocreator(var_ai_response, config.TTS_TOOL)

        var_df = func_core_subtitlescreator(var_temp_mp3)

        var_file = func_core_videocreator(var_ai_response, var_df, var_temp_mp3)
        var_title = (source+': '+var_title+' #News #'+source)

        var_file_history = open(config.PATH_TO_HISTORY_FILE,"a")
        var_file_history.write(str(var_title))
        var_file_history.close()

        #upload_video(file, description=title, cookies="cookies.txt")
        #func_tiktok_post(var_file, var_title)
    except Exception as e:
        print("Exception Occured",e)
        var_file_history = open(config.PATH_TO_HISTORY_FILE,"a")
        var_file_history.write(str(var_title))
        var_file_history.close()
