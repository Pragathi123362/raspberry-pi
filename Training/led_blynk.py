import RPi.GPIO as GPIO
import time


LED=16
#SW=18
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)                                                                                                                            
GPIO.setup(LED, GPIO.OUT)
#GPIO.setup(SW, GPIO.IN)
while(1):
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(1)                                                                        
# Infinite loop
#while True:
    #If GPIO.input(SW) == 0:
       # Turn off
       # GPIO.output(LED, GPIO.LOW)
   # else:
        # Turn on
       # GPIO.output(LED, GPIO.HIGH)'''
