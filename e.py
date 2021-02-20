import serial               #import serial pacakge
import time
import webbrowser           #import package for opening link in browser
import sys                  #import system package
from mcp3208 import MCP3208
import RPi.GPIO as GPIO
import sys
import urllib
##import Adafruit_DHT as dht
import requests
myAPI = 'MECLOBYQ0OH5YPXY' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
a=0
e="safe"
f="danger"
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


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

    




try:
    while True:
        x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        

        y = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        c= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        

        d= readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print (" P1 %s " % (y))

        z = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print( " P2 %s " % (z))
        print ((" x %s " % (x)),(" y %s " % (y)),(" z %s " % (z)))

        time.sleep(2)


        if x<1100 or x>1500 or y<1100 or y>1500:
                if a==0:
                        conn =urllib.request.urlopen(baseURL + '&field1=%s&field3=%s' % (x,y))
                        conn =urllib.request.urlopen(baseURL + '&field6=%s' % (f))
                        print("f:     ")
                        print(f)

        #print (conn.read())
                        
        
        # Closing the connection
                        conn.close()
                        time.sleep(2)
                        print("thingspeak uploaded")
                        print("patient in danger")

        else:
                conn =urllib.request.urlopen(baseURL + '&field4=%s&field5=%s' % (c,d))
              
                conn =urllib.request.urlopen(baseURL + '&field7=%s' % (e))
        #print (conn.read())
                print("e:     ")
                print(e)
        # Closing the connection
                conn.close()
                time.sleep(2)
                print("thingspeak uploaded")
##                a=0
                print("patient safe")
                        
except KeyboardInterrupt:
    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)
