import string
from glob import glob
import time
import datetime
import ssl
import os
import argparse
from articles import *
from utils import *
import config


argparser = argparse.ArgumentParser(description="AI Video Maker Script")
argparser.add_argument("--clean-history", type=str, help="delete the history file", default="no")
args = argparser.parse_args()


'''
pip install gTTS
pip install azure-cognitiveservices-speech
pip install openai
pip install feedparser
pip install moviepy
pip install git+https://github.com/openai/whisper.git
pip install pydub
pip install pycaption
pip install wheel
pip install playsound
pip install playwright
pip install opencv-python

playwright install

manual install of ffmpeg and ImageMagick on Windows

This Script has 5 main phases:
1. Fetches the latest political news from various sources (CNN, NYTimes, Washington Post, BBC).
2. Processes the news articles to create a summary using OpenAI or Azure OpenAI.
3. Converts the summary into speech using either Microsoft Azure's Text-to-Speech, Google TTS or TikTok API 
4. Creates a video with subtitles and a animated background video (randomly selecting a slice of a randomly selected mp4 video).
5. The last phase was to automatically post the video to TikTok. But this feature is currently disabled.

It expects the following folders to exist:

"F:\toker\videos\" - for storing the generated videos
"F:\toker\background\" - for storing the background videos (the videos must be named yt-1.mp4, yt-2.mp4, etc.)

I'm using the font 'P052-Bold' for subtitles, which should be available in your system. You can change the font by modifying the 'SUBTITLE_FONT' in the config.py file.
'''

# Main function that triggers the entire process
def main(param_themes):

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Starting main function...")
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    if os.path.exists(config.PATH_TO_HISTORY_FILE):
        filepost = open(config.PATH_TO_HISTORY_FILE,"r")
        history_articles = filepost.read()
        filepost.close()
    else:
        open(config.PATH_TO_HISTORY_FILE, 'a').close()
        history_articles = ''

    interval = 15 # Interval in seconds between processing each article

    # Commenting CNN as the RSS feed is not working properly
    #func_cnn_newsroom(themes, history_articles, interval)

    #func_nytimes_newsroom(param_themes, history_articles, interval)

    func_washingtonpost_newsroom(param_themes, history_articles, interval)

    func_bbc_newsroom(param_themes, history_articles, interval)


##################################### Script Start #####################################

# Removing old MP3 files
mp3files = glob((config.PATH_VIDEO_OUTPUT+'tempaudio_*.mp3'), recursive=True)

for mp3file in mp3files:
    os.remove(mp3file)


if args.clean_history.lower() == "yes":
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Deleting history file...")
    if os.path.exists(config.PATH_TO_HISTORY_FILE):
        os.remove(config.PATH_TO_HISTORY_FILE)
    open(config.PATH_TO_HISTORY_FILE, 'a').close()  # Create a new empty history file



# looping the main function to keep it running
while 1 == 1:
    try:
        main(config.NEWS_THEMES)
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Sleeping for 60 seconds")
        time.sleep(60)
    except Exception as e:
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Exception Occured",e)
        time.sleep(60)
        main(config.NEWS_THEMES)
