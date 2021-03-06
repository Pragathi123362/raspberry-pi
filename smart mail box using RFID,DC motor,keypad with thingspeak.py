import serial
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
from time import sleep
import sys
import urllib3
Motor1A = 16
Motor1B = 20
##myAPI = 'UQGMBO6Z050EGY4Y' 
### URL where we will send the data, Don't change it
##baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
i=0

RS = 5
EN = 8
D4 = 7
D5 = 1
D6 = 12
D7 = 6

HIGH=1
LOW=0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
GPIO.setup(Motor1B,GPIO.OUT)
GPIO .setup(RS,GPIO.OUT)
GPIO .setup(EN,GPIO.OUT)
GPIO .setup(D4,GPIO.OUT)
GPIO .setup(D5,GPIO.OUT)
GPIO .setup(D6,GPIO.OUT)
GPIO .setup(D7,GPIO.OUT)
def begin():
  lcdcmd(0x33) 
  lcdcmd(0x32) 
  lcdcmd(0x06)
  lcdcmd(0x0C) 
  lcdcmd(0x28) 
  lcdcmd(0x01) 
  sleep(0.0005)
 
def lcdcmd(ch): 
  GPIO.output(RS, 0)
  GPIO.output(D4, 0)
  GPIO.output(D5, 0)
  GPIO.output(D6, 0)
  GPIO.output(D7, 0)
  if ch&0x10==0x10:
    GPIO .output(D4, 1)
  if ch&0x20==0x20:
    GPIO .output(D5, 1)
  if ch&0x40==0x40:
    GPIO .output(D6, 1)
  if ch&0x80==0x80:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  sleep(0.005)
  GPIO .output(EN, 0)
  # Low bits
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x01==0x01:
    GPIO .output(D4, 1)
  if ch&0x02==0x02:
    GPIO .output(D5, 1)
  if ch&0x04==0x04:
    GPIO .output(D6, 1)
  if ch&0x08==0x08:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  sleep(0.005)
  GPIO .output(EN, 0)
  
def lcdwrite(ch): 
  GPIO .output(RS, 1)
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x10==0x10:
    GPIO .output(D4, 1)
  if ch&0x20==0x20:
    GPIO .output(D5, 1)
  if ch&0x40==0x40:
    GPIO .output(D6, 1)
  if ch&0x80==0x80:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  sleep(0.005)
  GPIO .output(EN, 0)
  # Low bits
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x01==0x01:
    GPIO .output(D4, 1)
  if ch&0x02==0x02:
    GPIO .output(D5, 1)
  if ch&0x04==0x04:
    GPIO .output(D6, 1)
  if ch&0x08==0x08:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  sleep(0.005)
  GPIO .output(EN, 0)
def lcdclear():
  lcdcmd(0x01)
 
def lcdprint(Str):
  l=0;
  l=len(Str)
  for i in range(l):
    lcdwrite(ord(Str[i]))
    
def setCursor(x,y):
    if y == 0:
        n=128+x
    elif y == 1:
        n=192+x
    lcdcmd(n)
 
def main():
  begin()
  lcdcmd(0x0F)
  lcdcmd(0x01)
    


myAPI = 'UQGMBO6Z050EGY4Y' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
ser = serial.Serial ("/dev/ttyS0", baudrate=9600)#Open port with baud rate and if in the shellshows like S0 is not enable then follow iot4beginners.com website and then follow the commands
count =0
KEYPAD = [
    ["1", "2"," 3"],
    ["4", "5", "6"],
    ["7","8","9"],
    ["*", "0", "#"]
]

ROW_PINS = [21,23,24,25] # BCM numbering
COL_PINS = [10, 9, 11] # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
print("press 1 or 2")
lcdcmd(0x01)
lcdprint("press 1 or 2")

def printKey(key):
   
    if(key=="1"):
      print(key)
      print("please swipe the card")
      lcdcmd(0x01)
      lcdprint("please swipe")
      lcdcmd(0xc0)
      lcdprint("the card")
      
      received_data = ser.read()              #read serial port
      sleep(0.03)
      data_left = ser.inWaiting()             #check for remaining byte
      received_data += ser.read(data_left)
      print (received_data)
        #print received data
      if received_data==b'2000F68B2B76':
        print("Card No - 1")
        print("WELCOME TO FLIPKART")
        print(" ")
        lcdcmd(0x01)
        lcdprint("WELCOME TO FLIPKART")
        sleep(1)
        lcdcmd(0x01)
        lcdprint("your card no : ")
        lcdcmd(0xc0)
        lcdprint("b'2000F68B2B76'")
       
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
     
        
        
        sleep(1)
        
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
        sleep(1)
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        sleep(1)
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
      
        http = urllib3.PoolManager()
        url = baseURL +'&field3=%s' % (received_data)
        print(url)
        resp = http.request('GET', url)
        
            
        sleep(2)
        print("press 1 or 2")
        lcdcmd(0x01)
        lcdprint("press 1 or 2")
       
      elif received_data==b'3600A4FBF29B':
        print("Card No - 2")
        print("WELCOME TO AMAZON")
        print(" ")
        lcdcmd(0x01)
        lcdprint("WELCOME TO AMAZON")
        sleep(1)
        lcdcmd(0x01)
        lcdprint("your card no : ")
        lcdcmd(0xc0)
        lcdprint("b'3600A4FBF29B'")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
     
        
        
        sleep(1)
        
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
        sleep(1)
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        sleep(1)
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.LOW)
        http = urllib3.PoolManager()
        url = baseURL +'&field3=%s' % (received_data)
        print(url)
        resp = http.request('GET', url)
##            print(resp.status)
            
        sleep(2)
##    elif received_data==b'3600A43C903E':
##        print("Card No - 3")
##        print("WELCOME TO MEESHO")
##        print(" ")
        print("press 1 or 2")
        lcdcmd(0x01)
        lcdprint("press 1 or 2")

      else:
        
        print("INVALID CARD")
        print("press 1 or 2")
        lcdcmd(0x01)
        lcdprint("INVALID CARD")
    if(key=="2"):
      print(key)
      print("please swipe the card")
      lcdcmd(0x01)
      lcdprint("please swipe")
      lcdcmd(0xc0)
      lcdprint("the card")
      received_data = ser.read()              #read serial port
      sleep(0.03)
      data_left = ser.inWaiting()             #check for remaining byte
      received_data += ser.read(data_left)
      print (received_data)
      if received_data==b'2000F68B2B76':
          print("Card No - 1")
          print("WELCOME TO FLIPKART")
          print(" ")
          lcdcmd(0x01)
          lcdprint("WELCOME TO FLIPKART")
          sleep(1)
          lcdcmd(0x01)
          lcdprint("your card no : ")
          lcdcmd(0xc0)
          lcdprint("b'2000F68B2B76'")
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.HIGH)
       
          
          
          sleep(1)
          
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.LOW)
          sleep(1)
          GPIO.output(Motor1A,GPIO.HIGH)
          GPIO.output(Motor1B,GPIO.LOW)
          sleep(1)
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.LOW)
          http = urllib3.PoolManager()
          url = baseURL +'&field4=%s' % (received_data)
          print(url)
          resp = http.request('GET', url)
##            print(resp.status)
              
          sleep(2)
          print("press 1 or 2")
          lcdcmd(0x01)
          lcdprint("press 1 or 2")
      elif received_data==b'3600A4FBF29B':
          print("Card No - 2")
          print("WELCOME TO AMAZON")
          print(" ")
          lcdcmd(0x01)
          lcdprint("WELCOME TO AMAZON")
          sleep(1)
          lcdcmd(0x01)
          lcdprint("your card no : ")
          lcdcmd(0xc0)
          lcdprint("b'3600A4FBF29B'")
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.HIGH)
       
          
          
          sleep(1)
          
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.LOW)
          sleep(1)
          GPIO.output(Motor1A,GPIO.HIGH)
          GPIO.output(Motor1B,GPIO.LOW)
          sleep(1)
          GPIO.output(Motor1A,GPIO.LOW)
          GPIO.output(Motor1B,GPIO.LOW)
          http = urllib3.PoolManager()
          url = baseURL +'&field4=%s' % (received_data)
          print(url)
          resp = http.request('GET', url)
##            print(resp.status)
              
          sleep(2)
          print("press 1 or 2")
          lcdcmd(0x01)
          lcdprint("press 1 or 2")
      else:
          print("INVALID CARD")
          print("please swipe the card")   

keypad.registerKeyPressHandler(printKey)
    
    
# printKey will be called each time a keypad button is pressed




    
         
