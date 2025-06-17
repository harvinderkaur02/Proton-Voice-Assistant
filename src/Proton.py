import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import app
import pyjokes
import pywhatkit
from threading import Thread
#---adding new modules
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume




# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("I am Proton, how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)
        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()

# Executes Commands (input: string)
def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    app.ChatBot.addUserMsg(voice_data)  # show full original message in GUI
    command = voice_data.replace('proton', '').strip() # Clean the trigger word



    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
        return

    # STATIC CONTROLS
    if 'hello' in voice_data:
        wish()
    elif 'what is your name' in voice_data:
        reply('My name is Proton!')
    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))
    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])
    elif 'search' in voice_data:
        query = voice_data.split('search', 1)[1]
        reply('Searching for ' + query)
        url = 'https://google.com/search?q=' + query
        try:
            webbrowser.open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')
    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.ChatBot.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio
        try:
            webbrowser.open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')
    elif 'bye' in voice_data or 'by' in voice_data:
        reply("Good bye Sir! Have a nice day.")
        is_awake = False
    elif 'exit' in voice_data or 'terminate' in voice_data:
        app.ChatBot.close()
        sys.exit()

        # Wikipedia Integration (final fixed version)
    elif any(phrase in command for phrase in ['who is', 'what is', 'tell me about']):
        query = None
        for phrase in ['who is', 'what is', 'tell me about']:
            if phrase in command:
                query = command.split(phrase, 1)[1].strip()
                break

        if not query:
            reply("Sorry, I didn't understand your question.")
            return

        try:
            print("Wikipedia Query:", query)
            reply(f"Searching Wikipedia for {query}...")
            summary = wikipedia.summary(query, sentences=2)
            reply(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            reply("Your query is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            reply("I couldn't find any result for your query.")
        except Exception as e:
            reply("Something went wrong while searching Wikipedia.")
            print("Wikipedia Error:", e)  


    #Screenshot Control
    elif 'screenshot' in command or 'take screenshot' in command:
        try:
            img = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(os.getcwd(), filename)
            img.save(filepath)
            reply(f"Screenshot saved as {filename}")
        except Exception as e:
            reply("Failed to take screenshot")
            print("Screenshot Error:", e)
    #remember feature
    elif 'remember that' in command or 'remember this' in command:
        reply("What should I remember?")
        memory = record_audio()
        if memory:
            with open('memory.txt', 'w') as f:
                f.write(memory)
            reply("I've remembered that.")

    elif 'what do you remember' in command or 'do you remember' in command:
        try:
            with open('memory.txt', 'r') as f:
                data = f.read()
            if data:
                reply(f"You told me to remember: {data}")
            else:
                reply("I don't have anything stored in memory.")
        except FileNotFoundError:
            reply("I don't remember anything yet.")


    # DYNAMIC CONTROLS
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
    elif 'paste' in voice_data or 'page' in voice_data or 'pest' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            print(f"{counter}: {f}")
            filestr += f"{counter}: {f}<br>"
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
    elif file_exp_status:
        counter = 0
        if 'open' in voice_data:
            try:
                index = int(voice_data.split(' ')[-1]) - 1
                selected = join(path, files[index])
                if isfile(selected):
                    os.startfile(selected)
                    file_exp_status = False
                else:
                    path = path + files[index] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += f"{counter}: {f}<br>"
                        print(f"{counter}: {f}")
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
            except:
                reply('You do not have permission to access this folder')
        elif 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a) + '//'
                files = listdir(path)
                for f in files:
                    counter += 1
                    filestr += f"{counter}: {f}<br>"
                    print(f"{counter}: {f}")
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
    # ---------- APP LAUNCHER ----------
    # ---------- APP LAUNCHER ----------
    elif 'open' in voice_data and not any(site in voice_data for site in ['youtube', 'instagram', 'linkedin', 'facebook', 'github']):

        print(f"App Launch Command: {command}")  # Debug print

        app_paths = {
            'notepad': 'notepad',
            'chrome': r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            'calculator': 'calc',
            'calc': 'calc',
            'cmd': 'start cmd',
            'command prompt': 'start cmd',
            'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            'excel': r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
        }

        launched = False
        for app_name, path in app_paths.items():
            if app_name in command:
                if path.endswith('.exe') or '\\' in path:
                    if os.path.exists(path):
                        os.startfile(path)
                        reply(f"Opening {app_name.title()}")
                    else:
                        reply(f"{app_name.title()} is not installed or path is incorrect.")
                else:
                    os.system(path)
                    reply(f"Opening {app_name.title()}")
                launched = True
                break

        if not launched:
            reply("I don't recognize this app. You can add more in the code!")
  #--------- youtube feature--------------------
    elif 'play' in command and 'on youtube' in command:
        song = command.replace('play', '').replace('on youtube', '').strip()
        reply(f"Playing {song} on YouTube")
        try:
            pywhatkit.playonyt(song)
        except Exception as e:
            reply("Something went wrong while opening YouTube.")
            print("YouTube Error:", e)

   #-----------joke feature--------------------
    elif 'joke' in command or 'funny' in command or 'make me laugh' in command:
        joke = pyjokes.get_joke()
        reply(joke)

 # ---------- OPEN SPECIFIC WEBSITE FEATURE ----------
    elif 'open' in voice_data:
        if 'youtube' in voice_data:
            webbrowser.open("https://www.youtube.com")
            reply("Opening YouTube")

        elif 'instagram' in voice_data:
            webbrowser.open("https://www.instagram.com")
            reply("Opening Instagram")

        elif 'linkedin' in voice_data:
            webbrowser.open("https://www.linkedin.com")
            reply("Opening LinkedIn")

        elif 'facebook' in voice_data:
            webbrowser.open("https://www.facebook.com")
            reply("Opening Facebook")

        elif 'github' in voice_data:
            webbrowser.open("https://www.github.com")
            reply("Opening GitHub")

        # Optional: add more websites here



        else:
            reply("I don't recognize this website. Please try a different name.")

    #-----Google search anything-----
    elif 'search' in voice_data:
        query = voice_data.split('search', 1)[1].strip()
        if query:
            reply(f"Searching Google for {query}")
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            reply("Here are the search results.")
        else:
            reply("What should I search for?")

    #-----Increaase/Decrease/Mute Feature------
    elif 'increase volume' in command or 'turn up the volume' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(current_volume + 0.1, 1.0)
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        reply("Volume increased.")

    elif 'decrease volume' in command or 'turn down the volume' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = max(current_volume - 0.1, 0.0)
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        reply("Volume decreased.")

    elif 'unmute volume' in command or 'unmute the sound' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        reply("Sound unmuted.")

    elif 'mute volume' in command or 'mute the sound' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
        reply("Sound muted.")




            
    else:
        reply('I am not functioned to do this!')

# ------------------Driver Code--------------------
t1 = Thread(target=app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None

while True:
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        voice_data = record_audio()

    if 'proton' in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successful")
            break
        except Exception as e:
            print(f"EXCEPTION raised while closing: {e}")
            break
