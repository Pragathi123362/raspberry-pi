import RPi.GPIO as GPIO
import threading
import serial               #import serial pacakge
import time
import webbrowser           #import package for opening link in browser
import sys                  #import system package
from mcp3208 import MCP3208
##from pulsesensor import Pulsesensor

import sys
import urllib

import requests
##p = Pulsesensor()
##p.startAsyncBPM()
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
import Adafruit_DHT

from Adafruit_IO import Client, Feed
a="normal temperature"
ADAFRUIT_IO_KEY = 'aio_pXrR84HTSGOInOPJlBIY1KlvNm7T'
ADAFRUIT_IO_USERNAME = 'Pragathi123'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
temp_feed=aio.feeds('temp')
salinelevel_feed=aio.feeds('salinelevel')
pposition_feed=aio.feeds('pposition')
ir=5
a=0
k=0
t=0
tem=0
s=0
sal=0
RS = 8
EN = 10
D4 = 12
D5 = 16
D6 = 32
D7 = 36

HIGH=1
LOW=0
tempp="temperature rises"
ntemp="normal temperature"
nsaline="saline level normal"
dsaline="saline level decreases"
psafe="patien safe"
pdanger="patiet in danger"
e="safe"
f="danger"
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24

#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO .setup(RS, GPIO .OUT)
GPIO .setup(EN, GPIO .OUT)
GPIO .setup(D4, GPIO .OUT)
GPIO .setup(D5, GPIO .OUT)
GPIO .setup(D6, GPIO .OUT)
GPIO .setup(D7, GPIO .OUT)

GPIO.setup(ir, GPIO.IN)

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
def begin():
  lcdcmd(0x33) 
  lcdcmd(0x32) 
  lcdcmd(0x06)
  lcdcmd(0x0C) 
  lcdcmd(0x28) 
  lcdcmd(0x01) 
  time.sleep(0.0005)
 
def lcdcmd(ch): 
  GPIO .output(RS, 0)
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
  time.sleep(0.005)
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
  time.sleep(0.005)
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
  time.sleep(0.005)
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
  time.sleep(0.005)
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
  print("hello")
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(14):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout  
          
def thread_function1():
    global s,sal
    while True:
        
        ir_val=GPIO.input(ir)
        #print(ir_val)
        if ir_val== 1:
            if s==0:
                
                lcdcmd(0x01)
 
    # Send some test
                lcdprint("saline level")
                lcdcmd(0xc3)
                lcdprint("    normal   ")
    
                time.sleep(2)
##                lcdcmd(0x01) # 1 second delay
                print('*************************saline level normal')
                time.sleep(1)
                aio.send(salinelevel_feed.key, str(nsaline))
                time.sleep(5)
                s=1
                sal=0
        else:
            if sal==0:
                 
                lcdcmd(0x01)
 
    # Send some test
                lcdprint("saline level")
                lcdcmd(0xc3)
                lcdprint("    decreases  ")
    
                time.sleep(2)
##                lcdcmd(0x01) # 1 second delay
                print('**************************saline level decreases')
                time.sleep(1)
                aio.send(salinelevel_feed.key, str(dsaline))
                time.sleep(5)
                sal=1
                s=0
            
           
            
        
    

def thread_function2():
    global a,k
    while True:
        
        x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        

        y = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)


        z = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        
        print ((" x %s " % (x)),(" y %s " % (y)),(" z %s " % (z)))

        time.sleep(1)


        if x<1100 or x>1500 or y<1100 or y>1500:
            if a==0:
                 lcdcmd(0x01)
 
    # Send some test
                 lcdprint("patient in ")
                 lcdcmd(0xc3)
                 lcdprint("    danger  ")
    
                 time.sleep(2)
##                 lcdcmd(0x01)
                 aio.send(pposition_feed.key, str(pdanger))
                 time.sleep(5)
                 print("______________________________________________thingspeak uploaded")
                 print("._____________________________________________patient in danger")
                 a=1
                 k=0

           

        else:
            if k==0:
                lcdcmd(0x01)
 
    # Send some test
                lcdprint("patient safe")
                time.sleep(2)
##                lcdcmd(0x01)
                aio.send(pposition_feed.key, str(psafe))
                time.sleep(5) 
                print("________________________________________thingspeak uploaded")

                print("._______________________________________patient safe")
                a=0
                k=1   
                 
def thread_function4():
    global t,tem
    while True:
        
        temperature = sensor.get_temperature()
        print("The temperature is %s celsius" % temperature)
        te=str(temperature)
        #print(ir_val)
        if temperature>32:
            
            if t==0:
                lcdcmd(0x01) 
                lcdprint("temp rises ")
##                lcdcmd(0xc3)
##                lcdprint("    rises  ")
    
                time.sleep(1)
##                lcdcmd(0x01) 
                print("..........................................temperature rises")
                time.sleep(0.5)
                aio.send(temp_feed.key, str(tempp))
                time.sleep(5)
                t=1
                tem=0
        else:
            if tem==0:
                
                lcdcmd(0x01) 
                lcdprint("temp normal ")
##                lcdcmd(0xc0)
##                lcdprint("    normal   ")
##    
                time.sleep(2)
##                 lcdcmd(0x01) 
                print("..........................................normal temperature")
                time.sleep(0.5)
                aio.send(temp_feed.key, str(ntemp))
                time.sleep(5)
                tem=1
                t=0

  
                  
                  
                  

thread1= threading.Thread(target=thread_function1)# args=(1,))

thread2= threading.Thread(target=thread_function2)


thread4= threading.Thread(target=thread_function4)
##
thread1.start()
thread2.start()
##
thread4.start()


   

   
        
        
                                          
                    
                           
