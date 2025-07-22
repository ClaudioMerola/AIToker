from gtts import gTTS
import os
import requests
#import azure.cognitiveservices.speech as speechsdk
from pydub.playback import play
from pydub.silence import split_on_silence
from pydub import AudioSegment
from pydub.effects import speedup
import playsound
import base64
import random
import string
import datetime
import config
from glob import glob

# This is the function that uses TikTok's API to convert text to speech.
def func_tiktok_texttospeach(session_id: str, text_speaker: str = "br_005", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    if(scode == 0):
        return output_data
    else:
        mp3files = glob((config.PATH_VIDEO_OUTPUT+'tempaudio_*.mp3'), recursive=True)
        for mp3file in mp3files:
            os.remove(mp3file)
        main(config.NEWS_THEMES)



    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Invoking Azure OpenAI")
    chat_completion = client.chat.completions.create(model="gpt-4.1", messages=[{"role": "system", "content": aiprompt}])

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Getting response from Azure OpenAI")
    return chat_completion.choices[0].message.content


# This is the core function that handles the audio creation using Microsoft Azure, Google TTS or TikTok's Text-to-Speech API.
def func_core_audiocreator(phrase: str, param_tts: str):
    char_set = string.ascii_uppercase + string.digits
    if(param_tts == 'MS'):
        speech_config = speechsdk.SpeechConfig(subscription=config.AZURE_SUBSCRIPTION_KEY, region=config.AZURE_REGION)
        speech_config.speech_synthesis_voice_name = config.AZURE_VOICE

    # Audio creation

    print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Audio Creation")
    # Checking if Text to Speech is Microsoft or Google (or TikTok if neither)
    if(param_tts == 'MS'):
        wavfile = ''.join(random.sample(char_set*6, 6))
        #speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "sdklog.log")
        wavfile = (config.PATH_VIDEO_OUTPUT+wavfile+'.wav')
        file_config = speechsdk.audio.AudioOutputConfig(filename=wavfile)
        #audio_config = speechsdk.audio.AudioOutputConfig(filename="F:\toker\videos\output.wav")
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

        func_azure_text_to_speech(phrase, wavfile)

        # MP3 Conversion
        tempmp3 = ''.join(random.sample(char_set*6, 6))
        tempmp3 = (config.PATH_VIDEO_OUTPUT+tempmp3+'.mp3')
        sound = AudioSegment.from_wav(wavfile)
        sound.export(tempmp3, format="mp3", bitrate='192k')

    elif(param_tts == 'Google'):
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Using Google TTS")
        tempmp3 = ''.join(random.sample(char_set*6, 6))
        tempmp3 = (config.PATH_VIDEO_OUTPUT+tempmp3+'.mp3')
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Creating audio with Google TTS")
        GoogleAudio = gTTS(text=phrase,slow=False,lang='en',tld='us')
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Saving audio to MP3")
        GoogleAudio.save(tempmp3)
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Speeding up audio")
        audio = AudioSegment.from_mp3(tempmp3)
        new_file = speedup(audio,1.3,150)
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Exporting audio to MP3")
        new_file.export(tempmp3, format="mp3")
    else:
        prhase = phrase.replace(', ','. ')
        words = phrase.split('. ')
        tempaudio = 1
        for word in words:
            tempword = len(word.split(' '))
            if(tempword > 20):
                tempword2 = word.split(' of ')
                if(len(tempword2) < 2):
                    tempword3 = word.split(' the ')
                    for w in tempword3:
                        tempfile = (config.PATH_VIDEO_OUTPUT+'tempaudio_'+str(tempaudio)+'.mp3')
                        func_tiktok_texttospeach(config.TIKTOK_SESSION_ID, config.TIKTOK_VOICE , w, tempfile, False)
                        tempaudio += 1
                else:
                    for w in tempword2:
                        tempfile = (config.PATH_VIDEO_OUTPUT+'tempaudio_'+str(tempaudio)+'.mp3')
                        func_tiktok_texttospeach(config.TIKTOK_SESSION_ID, config.TIKTOK_VOICE , w, tempfile, False)
                        tempaudio += 1
            else:
                tempfile = (config.PATH_VIDEO_OUTPUT+'tempaudio_'+str(tempaudio)+'.mp3')
                func_tiktok_texttospeach(config.TIKTOK_SESSION_ID, config.TIKTOK_VOICE , word, tempfile, False)
                tempaudio += 1

        mp3files = glob(config.PATH_VIDEO_OUTPUT+'tempaudio_*.mp3', recursive=True)

        tempmp3 = ''.join(random.sample(char_set*6, 6))
        tempmp3 = (config.PATH_VIDEO_OUTPUT+tempmp3+'.mp3')

        clips = [AudioFileClip(c) for c in mp3files]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(tempmp3)

        for mp3file in mp3files:
            os.remove(mp3file)

    return tempmp3


# Function to convert text to speech using Azure's Text-to-Speech service.
def func_azure_text_to_speech(text, wavfile):
    result = synthesizer.speak_text_async(text).get()

    # Saving the audio output to a file
    #output_file = "F:\toker\videos\output.wav"
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - wav File created: "+wavfile)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
