import os
import time
#import playsound
import speech_recognition as sr
#from gtts import gTTS
import pyttsx3
#from google_calendar import *

'''Enables voice for the bot'''
def bot_speak(text):
    mouth = pyttsx3.init()
    mouth.say(text)
    mouth.runAndWait()

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

bot_speak('hello')
