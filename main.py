import os
import time
import playsound
import pyttsx3
import speech_recognition as sr
from gtts import gTTS

'''Enables voice for the bot'''
def bot_speak(text):
    #Transforms text to audio
    both_mouth = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    both_mouth.save(filename)
    playsound.playsound(filename)

'''Get/Listens to user's voice'''
def bot_ear():
    r = sr.Recognizer()
    with sr.Microphone() as voice:
        audio = r.listen(voice)
        word = ""

        try:
            #Fetch Google API to recognize voice
            word = r.recognize_google(audio)
            print(word)
        except Exception as e:
            print("Exception" + str(e))

        return word
    
text = bot_ear()

if "hello" in text:
    bot_speak("Hello Quin, how are you ?")
