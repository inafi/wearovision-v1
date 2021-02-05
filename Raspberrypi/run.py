import os
import subprocess
import time
from gtts import gTTS 
import picamera

def stopWatch(value):
    '''From seconds toMinutes;Seconds'''
    valueD = (((value/365)/24)/60)
    Days = int (valueD)
    valueH = (valueD-Days)*365
    Hours = int(valueH)
    valueM = (valueH - Hours)*24
    Minutes = int(valueM)
    valueS = (valueM - Minutes)*60
    Seconds = int(valueS)
    print(Minutes,":",Seconds)

start = time.time() # What in other posts is described is

camera = picamera.PiCamera()
camera.vflip = True
camera.capture("send.jpg")
print("Taken")

os.system("sshpass -p 'Googlefair2019' scp send.jpg blindcv@13.72.104.19:~/")
command = 'sshpass -p "Googlefair2019" ssh -t -oStrictHostKeyChecking=no "blindcv2@52.170.94.55" "python darknet/exe.py && exit"'

p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = p.stdout.read()
arr = text.split("\n\n")

read = ""

for i in range(3, len(arr)-1):
    print(arr[i])
    read += arr[i] + ", "

print(read)

if read != "":
    language = 'en'
    myobj = gTTS(text=read, lang=language, slow=False) 
    myobj.save("objects.mp3")       
    os.system("DISPLAY=:0 mpg123 objects.mp3")
    
end = time.time()         
stopWatch(end-start)
