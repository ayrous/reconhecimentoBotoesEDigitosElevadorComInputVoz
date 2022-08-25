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
        if i == "oitavo" or i == "oito" or i == "topo" or i == "8":
            buscaUm = 8
        elif i == "sétimo" or i == "setimo" or i == "sete" or i == "7":
            buscaUm = 7
        elif i == "sexto" or i == "seis" or i == "6":
            buscaUm = 6
        elif i == "quinto" or i == "cinco" or i == "5":
            buscaUm = 5
        elif i == "quatro" or i == "quatro" or i == "4":
            buscaUm = 4
        elif i == "terceiro" or i == "três" or i == "3":
            buscaUm = 3
        elif i == "segundo" or i == "dois" or i == "2":
            print("entrou no dois")
            buscaUm = 2
        elif i == "primeiro" or i == "um" or i == "1":
            buscaUm = 1
        elif i == "terreo" or i == "zero" or i == "térreo" or i == "piso vermelho" or i == "0":
            buscaUm = 0
    
    if buscaUm == -1:
        speak("Não entendi o andar, fale novamente, por favor")
        frase = get_audio()
        buscaUm = verificaAndar(frase)    
    else:
        speak("Beleza, vamos para o " + str(buscaUm))
        return buscaUm

for mic in sr.Microphone.list_microphone_names():
    print(mic)

def main():
    speak("Olá, para onde quer ir?!")

    frase = get_audio()
    busca = verificaAndar(frase)
    return busca

#if busca == -1:
 #   speak("Não entendi o andar, fale novamente, por favor")
  #  frase = get_audio()
   # busca = verificaAndar(frase)