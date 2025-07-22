import whisper #openai-whisper
import os
from mutagen.mp3 import MP3
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import *
from moviepy.video.fx.resize import resize
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg
from pycaption import CaptionConverter
import pandas as pd
import random
import string
import datetime
import config

# This is the core function that processes the MP3 file and creates subtitles.
def func_core_subtitlescreator(tempmp3: str):

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Entering whisper")
    # Instantiate whisper model using model_type variable
    model = whisper.load_model('base')

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Starting to analyze MP3 file")
    # Get text from speech for subtitles from audio file
    result = model.transcribe(tempmp3)

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Processing transcription results")
    # create Subtitle dataframe, and save it
    dict1 = {'start':[], 'end':[], 'text':[]}
    for i in result['segments']:
        dict1['start'].append(int(i['start']))
        dict1['end'].append(int(i['end']))
        dict1['text'].append(i['text'])
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Starting DF")
    df = pd.DataFrame.from_dict(dict1)

    return df

# This is the core function that handles the text-to-speech conversion and video creation.
def func_core_videocreator(phrase: str, df, tempmp3: str):

    phrases = [phrase]
    char_set = string.ascii_uppercase + string.digits
    # Merging Video and Audio
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Formatting Subtitles")
    generator = lambda txt: TextClip(txt, font=config.SUBTITLE_FONT, fontsize=35, stroke_width=.7, color='white', stroke_color = 'white', size = (1080, 1920*.25), method='caption')
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Creating Subtitles Clip")
    subs = tuple(zip(tuple(zip(df['start'].values, df['end'].values)), df['text'].values))
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Subtitles Clip created")
    subtitles = SubtitlesClip(subs, generator)

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Randomly selecting background video")
    backgroundvideo = random.randint(1, config.BACKGROUND_VIDEOS_COUNT)
    backgroundvideo = str(backgroundvideo)

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Searching for audio file: "+tempmp3)
    audio = MP3(tempmp3)
    audioduration = audio.info.length
    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Total audio duration: "+str(audioduration))

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Randomly selecting start time for video clip")
    start_time_video = random.randint(32, 432)
    end_time_video = (start_time_video + audioduration)

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Extracting video clip from background: yt-"+backgroundvideo+" from "+str(start_time_video)+" to "+str(end_time_video))
    ffmpeg_extract_subclip(
            (config.PATH_BACKGROUND_VIDEOS+'yt-'+backgroundvideo+'.mp4'),
            start_time_video,
            end_time_video,
            targetname=(config.PATH_BACKGROUND_VIDEOS+'backgroundtmp.mp4'),
        )


    generic_video = VideoFileClip(config.PATH_BACKGROUND_VIDEOS+'backgroundtmp.mp4')
    generic_video = generic_video.fx(vfx.loop, duration=audioduration)

    generic_video = generic_video.crop(x1=420, y1=0, width=1080, height=1920)
    generic_video = generic_video.margin(top=400)
    #generic_video = generic_video.set_subtitles(output_subtitles.srt)
    audio_clips = [AudioFileClip(tempmp3) for _ in phrases]
    final_clip = concatenate_audioclips(audio_clips)
    final_clip = final_clip.set_fps(generic_video.fps)
    final_clip = final_clip.set_duration(audioduration)

    logo = (ImageClip(config.PATH_TO_SCREENSHOT+"NewsScreenShot.png")
            .set_duration(audioduration)
            #.resize(width=800,height=350)
            .margin(right=8, top=2, opacity=1) # (optional) logo-border padding
            .set_pos(("center","top")))

    videofile = ''.join(random.sample(char_set*6, 6))
    result_video = generic_video.set_audio(final_clip)
    result_video = CompositeVideoClip([result_video, subtitles.set_position(('center',220)), logo])
    result_video.write_videofile((config.PATH_VIDEO_OUTPUT+videofile+'.mp4'), codec='libx264')
    result_video.close()


    # Deleting Temp Files

    os.remove(tempmp3)

    return (config.PATH_VIDEO_OUTPUT+videofile+'.mp4')

