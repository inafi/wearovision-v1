import io
import os
from google.cloud import vision
from google.cloud.vision import types
import enchant
import re

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/nafi/GSF-BlindCV-dbe904c5a134.json"
# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(os.path.dirname(__file__), 'gsf/data/otter.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
reply = client.text_detection(image=image)
labels = reply.text_annotations

#Sets up dictionary to see if string is english word
d = enchant.Dict("en_US")

#if empty description (no text detected) than it throws exception
try:    
    #Gets text from image json from google api
    text = next(iter(labels)).description

    #Filters through text and removes special charachters, empty strings, and lowercases
    words = (text.replace("\n", " ")).split(" ")
    for i in range(len(words)):
        words[i] = (re.sub(r"[^a-zA-Z0-9]","",words[i])).lower()
    words = list(filter(None, words)) 

    #Final reponse - checks to see if all strings are words otherwise return no
    response = ""

    #Removes strings that are not english words
    for i in range(len(words)-1, -1, -1):
        if not d.check(words[i]):
            del words[i]
    response = " ".join(str(x) for x in words)
except:
    response = "no text found"

print(response)
