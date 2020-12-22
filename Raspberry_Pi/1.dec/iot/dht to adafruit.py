import sys
import Adafruit_DHT
import RPi.GPIO as IO
from Adafruit_IO import Client, Feed
import time
from time import sleep
IO.setwarnings(False)
IO.setmode(IO.BCM) 
pin=4
ADAFRUIT_IO_KEY = 'aio_dTVP24SwqPrCcPZ6OLZkvLZ6uzkP'
ADAFRUIT_IO_USERNAME = 'Pragathi123'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
humidity_feed = aio.feeds('humidity')
temp_feed=aio.feeds('temp')
humidit_feed = aio.feeds('button1')
tep_feed=aio.feeds('voice')
IO.setup(pin,IO.OUT)
while True:
    humidity, temperature = Adafruit_DHT.read_retry(11,pin)
    sleep(1)
    tem=str(temperature)
    hum=str(humidity)
    print("temp"  ,temperature)
    print("humidity"  ,humidity)
    aio.send(temp_feed.key, str(temperature))
    aio.send(humidity_feed.key, str(humidity))
    aio.send(tep_feed.key, str(temperature))
    aio.send(humidit_feed.key, str(humidity))
    sleep(5)

    
