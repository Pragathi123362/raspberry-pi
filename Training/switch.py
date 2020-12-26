import RPi.GPIO as GPIO
import time

LED=16
SW=18
#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SW, GPIO.IN,GPIO.PUD_UP)

for i in range(5):
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(0.5)

# Infinite loop
while True:
    sw_val=GPIO.input(SW)
    
    if sw_val== 0:
        # Turn off
        GPIO.output(LED, GPIO.HIGH)
        print('switch pressed')
        time.sleep(0.5)
    else:
        # Turn on
        GPIO.output(LED, GPIO.LOW)
        time.sleep(0.5)
