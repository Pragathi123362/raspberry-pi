import os
import time
import serial
import sys

import urllib3

import sys   
import busio
import digitalio

import board
import RPi.GPIO as GPIO 
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pulsesensor import Pulsesensor
myAPI = "006JRMRBM7F5952J"
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(myAPI)
##

#Setup our API and delay

ir=26

RS = 7
EN = 6
D4 = 13
D5 = 19
D6 = 20
D7 = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO .setup(RS, GPIO .OUT)
GPIO .setup(EN, GPIO .OUT)
GPIO .setup(D4, GPIO .OUT)
GPIO .setup(D5, GPIO .OUT)
GPIO .setup(D6, GPIO .OUT)
GPIO .setup(D7, GPIO .OUT)
GPIO.setup(ir, GPIO.IN)

##    while True:
##        print("hello world")
##        lcdcmd(0x01)
## 
##    # Send some test
##        lcdprint("Electronics Hub ")
##        lcdcmd(0xc0)
##        lcdprint("    Presents    ")
##
##
##        time.sleep(2) # 2 second delay
##    

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P1)
chan1 = AnalogIn(mcp, MCP.P2)
chan2 = AnalogIn(mcp, MCP.P3)
last_read = 0       # this keeps track of the last potentiometer value
tolerance = 250     # to keep from being jittery we'll only change
                    # volume when the pot has moved a significant amount
p = Pulsesensor()
p.startAsyncBPM()
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
def begin():
  lcdcmd(0x33) 
  lcdcmd(0x32) 
  lcdcmd(0x06)
  lcdcmd(0x0C) 
  lcdcmd(0x28) 
  lcdcmd(0x01) 
  time.sleep(0.0005)
 
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
    
while True:
   
    #print("bbbbbbbbbb")
    ir_val=GPIO.input(ir)
    print('x', chan0.value)

    print('y: ', chan1.value)

    print('z: ', chan2.value)

    time.sleep(1)
   
    temperature = sensor.get_temperature()
    t=str(temperature)
    print("The temperature is %s celsius" % temperature)
    if temperature>33:
       

        print("adafruit")
        lcdcmd(0x01)
        lcdprint("temp high")
        time.sleep(1)
        print("tep high")
##        conn =urllib.request.urlopen(baseURL + '&field1=%s' % (temperature))
##        conn.close()
        thingspeakHttp = BASE_URL + "&field1={:.2f}".format(temperature)
        print(thingspeakHttp)

            
##        conn = urllib.request.urlopen(thingspeakHttp)
##        print("Response: {}".format(conn.read()))
##        conn.close()
        http = urllib3.PoolManager()
        url = BASE_URL + "&field1={:.2f}".format(temperature)
        resp = http.request('GET', url)
        #print(resp.status)
            
        time.sleep(5)
    else:
        lcdcmd(0x01)
        lcdprint("temp normal")
        time.sleep(1)
        print("normal temperature")
        thingspeakHttp = BASE_URL + "&field1={:.2f}".format(temperature)
        print(thingspeakHttp)

            
##        conn = urllib.request.urlopen(thingspeakHttp)
##        print("Response: {}".format(conn.read()))
##        conn.close()
        http = urllib3.PoolManager()
        url = BASE_URL + "&field1={:.2f}".format(temperature)
        resp = http.request('GET', url)
        #print(resp.status)
            
        time.sleep(5)
       
   
    bpm = p.BPM
    if bpm >0:
        print("BPM: %d" % bpm)
        if bpm>90:
          lcdcmd(0x01)
          lcdprint("BPM high")
          time.sleep(1)
          print("high")
          thingspeakHttp = BASE_URL + "&field2={:.2f}".format(bpm)
          print(thingspeakHttp)
          http = urllib3.PoolManager()
          url = BASE_URL + "&field2={:.2f}".format(bpm)
          resp = http.request('GET', url)
        
          time.sleep(5)
           
        else:
          thingspeakHttp = BASE_URL + "&field2={:.2f}".format(bpm)
          print(thingspeakHttp)
          http = urllib3.PoolManager()
          url = BASE_URL + "&field2={:.2f}".format(bpm)
          resp = http.request('GET', url)
        
          time.sleep(5)
           
            
    else:
      
      print("No Heartbeat found")
      time.sleep(1)
    if chan0.value>25024 or chan0.value<18176 or chan1.value>25400 or chan1.value<19200:
      
      print("fallen");
      time.sleep(2)
      lcdcmd(0x01)
      lcdprint("patient in ")
      lcdcmd(0xc0)
      lcdprint("danger")
      thingspeakHttp = BASE_URL + "&field3={:.2f}".format(chan0.value)
      print(thingspeakHttp)
      http = urllib3.PoolManager()
      url = BASE_URL + "&field3={:.2f}".format(chan0.value)
      resp = http.request('GET', url)
        
      time.sleep(5)
    else:
      print("safe")
      time.sleep(2)
      lcdcmd(0x01)
      lcdprint("patient safe")
      time.sleep(1)
      thingspeakHttp = BASE_URL + "&field3={:.2f}".format(chan0.value)
      print(thingspeakHttp)
      http = urllib3.PoolManager()
      url = BASE_URL + "&field3={:.2f}".format(chan0.value)
      resp = http.request('GET', url)
        
      time.sleep(5)

    
        #print(ir_val)
    if ir_val== 1:
        print('*************************saline level normal')
        time.sleep(1)
        lcdcmd(0x01)
        lcdprint("saline normal")
        time.sleep(1)
        thingspeakHttp = BASE_URL + "&field7={:.2f}".format(ir_val)
        print(thingspeakHttp)
        http = urllib3.PoolManager()
        url = BASE_URL + "&field7={:.2f}".format(ir_val)
        resp = http.request('GET', url)
        time.sleep(5)
      
##                aio.send(salinelevel_feed.key, str(nsaline))
##                time.sleep(5)
##                s=1
        
##                sal=0
    else:
        lcdcmd(0x01)
        lcdprint("saline decreases")
        time.sleep(1)
        print('**************************saline level decreases')
        time.sleep(1)
        thingspeakHttp = BASE_URL + "&field7={:.2f}".format(ir_val)
        print(thingspeakHttp)
        http = urllib3.PoolManager()
        url = BASE_URL + "&field7={:.2f}".format(ir_val)
        resp = http.request('GET', url)
        time.sleep(5)
##                aio.send(salinelevel_feed.key, str(dsaline))
##                time.sleep(5)
##                sal=1
##                s=0
##            
               

