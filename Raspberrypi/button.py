import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

s = 0
p = 0
count = 0
while True:
    if GPIO.input(14) == GPIO.HIGH:
        s = 0
    elif s == 0:
        s = 1
        count += 1
        print(count - 1)
        if count > 0:
            os.system("python3 run.py")
            print("Ran\n")
GPIO.cleanup()