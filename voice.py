import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    r.adjust_for_ambient_noise(source)
    audio=r.listen(source)
text = r.recognize_google(audio)
text=text.lower()
print(text)

def returnobj(s):
    t = s.split("search for my ")
    return t[1]

if "carol search for my" in text or "search for my" in text:
    type(len(text))
    response = "looking for "+ returnobj(text)
elif "scan the area" in text:
    response = "Scanning"
elif "search for text" in text:
    response = "Searching"
else:
    response = "Sorry I didn't catch that"

engine = pyttsx3.init()
engine.say(response)
engine.runAndWait()