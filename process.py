'''Manipulate local computer's execution'''

import subprocess
from bot import *

TAKE_NOTE_CMDS = ["open a note", "take a note", "make a note", "write these down", "remember this"]
def take_note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"

    with open(file_name, "w") as f:
        f.write(text)

    word = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\word.exe"
    subprocess.Popen([word, file_name])

print("Sammy is ready now. Please ask something")
text = bot_ear().lower()
for phrase in TAKE_NOTE_CMDS:
    if phrase in text.lower():
        bot_speak("Ok beauty. What do you want me to write down ?")
        note_text = bot_ear().lower()
        take_note(note_text)
        bot_speak("Ok I am done. I have taken note for that")
    else:
        bot_speak("Oh..I do not get it. Please try again.")
