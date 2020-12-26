import lcd
import time
import RPi.GPIO as GPIO
RS = 26
EN = 19
D4 = 13
D5 = 6
D6 = 5
D7 = 1
mylcd=lcd.lcd()
mylcd.begin(D4,D5,D6,D7,RS,EN)
mylcd.Print("How are you")
time.sleep(2)
while True:
  mylcd.clear()
  mylcd.Print("I am RaspberryPi") 
  mylcd.setCursor(2,1)
  mylcd.Print("Electro-Passion")
  time.sleep(2)
  mylcd.clear()
  mylcd.Print("Seconds=")
  seconds=0
  mylcd.setCursor(1,9)
  mylcd.Print(seconds)
  mylcd.shift(mylcd.right,5)
  mylcd.shift(mylcd.left,5)
  mylcd.blinkCursorOn()
  time.sleep(2)
  mylcd.blinkCursorOff()
