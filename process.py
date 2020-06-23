'''Manipulate local computer's execution'''

from google_calendar import *
from bot import *


SERVICE = authenticate_google()
print("Sammy is ready now. Please ask something")

WAKE = "hi sam"
while True:
    print("Sam is listening")
    text = bot_ear()

    if text.count(WAKE)>0:
        bot_speak("Hello. I am ready. Do you need me to do anything beauty?")
        text = bot_ear()
        
        CALENDAR_CMDS =["what do i have", "what is my plan", "do i have plan", "am i busy", "do i have any plan"]
        for phrase in CALENDAR_CMDS:
            if phrase in text:
                date = get_date(text)
                if date:
                    get_calendar_events(get_date(text), SERVICE)
                else:
                    bot_speak("Eventhough I do not get you but I think that you look really cute today")
                    break

        TAKENOTE_CMDS =["open a note", "take a note", "make a note", "write these down", "remember this"]
        for phrase in TAKENOTE_CMDS:
            if phrase in text:
                bot_speak("Ok beauty. What do you want me to write down ?")
                note_text = bot_ear().lower()
                take_note(note_text)
                bot_speak("Ok I am done. I have taken note for that")
            else:
                bot_speak("Oh..I do not get it. Please try again.")
                break
