# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import pickle
import os.path
import pytz
import subprocess

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bot import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAY_EXTENSIONS = ['st', 'nd', 'rd', 'th']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',]
MONTHS = ['january','february','march','april','may','june','july','august','september','october','november','december']

def authenticate_google():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_calendar_events(day, service):

    #Initialize time boundary (start and end time during day) for searching
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())

    utc = pytz.UTC      #Get current UTC timezone
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("freee")
        bot_speak("You do not have any events today. But dont worry, you always have me by your side.")
    else:
        bot_speak(f"Hello Beauty. You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                #Avoid bugs
                if start_time.split(":")[1] == "00":
                    start_time = str(int(start_time.split(":")[0]))
                    start_time = start_time + "am"
                else:
                    start_time = str(int(start_time.split(":")[0])) + start_time.split(":")[1]
                    start_time = start_time + "am"
            else:
                if start_time.split(":")[1] == "00":
                    start_time = str(int(start_time.split(":")[0])-12)
                    start_time = start_time + "pm"
                else:
                    start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                    start_time = start_time + "pm"

            bot_speak(event["summary"] + " at " + start_time)

def get_date(text):
    text = text.lower()
    #Get today's date
    today = datetime.date.today()
    #Break up text into different words
    if text.count("today")>0:
        return today

    #Initialize variables for day
    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    #Start iterating through voice's input to find keywords for date, month and year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found>0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    #When given month is less than today's month
    if month < today.month and month !=-1:
        year = year + 1

    #When day is less than today and month is not defined
    if day < today.day and day != -1 and month ==-1:
        month = month+1

    #When only day of weeks is given
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()   #Mon-Sun/0-6
        dif = day_of_week - current_day_of_week
        if dif<0:
            dif+=7      #Move to same day of week on next week
            if text.count("next") >=1:
                dif += 7

        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)

def take_note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"

    with open(file_name, "w") as f:
        f.write(text)

    notepad = "C:\\Users\\quynhhgoogoo\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad.exe"
    subprocess.Popen([notepad, file_name])


            
