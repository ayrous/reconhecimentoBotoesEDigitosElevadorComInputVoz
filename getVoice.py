import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pyaudio


def speak(txt):
    tts = gTTS(text=txt, lang="pt")
    filmename = "voice.mp3"
    tts.save(filmename)
    playsound.playsound(filmename)

def get_audio():
    # inicializa o reconhecimento
    r = sr.Recognizer()
    mic = sr.Microphone()
    audio= ''
    with mic as source:
        audio = r.listen(source,  phrase_time_limit = 0)
        said = ""
        print("entrou")
        try:
#            time.sleep(1.5)
            print("digaa")
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("error: "+str(e))
    
    return said

speak("Olá, para onde quer ir?!")
for mic in sr.Microphone.list_microphone_names():
    print(mic)

get_audio()