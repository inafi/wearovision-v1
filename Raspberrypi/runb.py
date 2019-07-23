import os
import subprocess
import time
from gtts import gTTS 
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

s = 0
p = 0
t = 0
count = 0

def run():
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.capture("send.jpg")
    print("Pic taken\n")
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

    os.system("sshpass -p 'Googlefair2019' scp send.jpg blindcv@13.72.104.19:~/")
    command = 'sshpass -p "Googlefair2019" ssh -t -oStrictHostKeyChecking=no "blindcv@13.72.104.19" "python darknet/exe.py && exit"'

    p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = p.stdout.read()
    arr = text.split("\n\n")
    print(arr)
    print("\n")

    read = ""

    for i in range(3, len(arr)-1):
        print(arr[i])
        read += arr[i] + ", "

    print(read)
    language = 'en'
    myobj = gTTS(text=read, lang=language, slow=False) 
    myobj.save("objects.mp3") 
      
    os.system("DISPLAY=:0 mpg123 objects.mp3")
    end = time.time()         
    stopWatch(end-start)

while True:
    if GPIO.input(14) == GPIO.HIGH:
        s = 0
    elif s == 0:
        s = 1
        if t == 1:
            count += 1
            print(count)
            run ()
            print("Ran\n")
        t = 1
        
GPIO.cleanup()
