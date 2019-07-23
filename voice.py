import speech_recognition as sr
import pyttsx3
import multiprocessing as mp
import os
import subprocess
import signal

r = sr.Recognizer()
mic = sr.Microphone()

response = ""

def runtext():
    command = "python exe-text.py"
    p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    print("text: ", "\n", text)

def saytext():
    reply = "Searching for text"
    engine = pyttsx3.init()
    engine.say(reply)
    engine.runAndWait()


with mic as source:
    r.adjust_for_ambient_noise(source)
    audio=r.listen(source)

try:
    text = r.recognize_google(audio)
    text=text.lower()
    print(text)

    if "carol search for my" in text or "search for my" in text:
        type(len(text))
        response = "looking for " + text.split("search for my ")[1]
    elif "scan the area" in text:
        response = "Scanning"
    elif "search for text" in text:
        p1 = mp.Process(target = runtext)
        p2 = mp.Process(target = saytext)

        p1.start()
        p2.start()
        p1.join()
        p2.join()
    else:
        response = "Sorry I didn't catch that"
except:
    response = "Sorry I didn't catch that"

engine = pyttsx3.init()
engine.say(response)
engine.runAndWait()