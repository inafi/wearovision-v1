import RPi.GPIO as GPIO, time
# Tell the GPIO library to use # Broadcom GPIO references
GPIO.setmode(GPIO.BCM)
# Define function to measure charge time
def RCtime (PiPin):
    measurement = 0
    # Discharge capacitor
    GPIO.setup(PiPin, GPIO.OUT)
    GPIO.output(PiPin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(PiPin, GPIO.IN)
    # Count loops until voltage across # capacitor reads high on GPIO
    while (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1
    return measurement
# Main program loop
prev = 0
once = True
while True:
    ldr = RCtime(14)
    if once:
        prev = ldr
        once = False
    print (ldr, prev)
    if ldr - prev > 800 and ldr > 1100 and prev < 1100:
        print("yes")
    if prev - ldr > 800 and ldr < 1100 and prev > 1100:
        print("no")
        #camera.stop_preview()
    prev = ldr