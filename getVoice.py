import nltk
nltk.download('punkt')
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
    print("vai entrar no WITH")
    with mic as source:
        print("entrou")
#        audio = r.listen(source,  phrase_time_limit = 0)
        r.adjust_for_ambient_noise(source, duration = 1)
        said = ""
        print("ajustou ambiente")
        audio = r.listen(source)
        try:
            print("reconhecimento")
            said = r.recognize_google(audio, language="pt-BR")
            print(said)
        except Exception as e:
            print("error: "+str(e))

    tokens = nltk.word_tokenize(str(said))
    
    return tokens

def verificaAndar(tokens):

    buscaUm = -1
    for i in tokens:
        if i == "oitavo" or i == "oito" or i == "topo":
            buscaUm = 8
        if i == "sétimo" or i == "setimo" or i == "sete":
            buscaUm = 7
        if i == "sexto" or i == "seis":
            buscaUm = 6
        if i == "quinto" or i == "cinco":
            buscaUm = 5
        elif i == "quatro" or i == "quatro":
            buscaNum = 4
        elif i == "terceiro" or i == "três":
            buscaUm = 3
        elif i == "segundo" or i == "dois":
            buscaUm == 2
        elif i == "primeiro" or i == "um":
            buscaUm = 1
        elif i == "terreo" or i == "zero" or i == "térreo" or i == "piso vermelho":
            buscaUm = 0
    
    if buscaUm == -1:
        speak("Não entendi o andar, fale novamente, por favor")
        frase = get_audio()
        buscaUm = verificaAndar(frase)    
    else:
        speak("Beleza, vamos para o " + str(buscaUm))
        return buscaUm

speak("Olá, para onde quer ir?!")
for mic in sr.Microphone.list_microphone_names():
    print(mic)

frase = get_audio()

busca = verificaAndar(frase)
#if busca == -1:
 #   speak("Não entendi o andar, fale novamente, por favor")
  #  frase = get_audio()
   # busca = verificaAndar(frase)