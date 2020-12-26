
import time
import RPi.GPIO as GPIO

################ thingspeak ###########
import requests
import urllib

url='https://api.thingspeak.com/update?api_key=ZI0HAENOOZWK9WEF&field4='
#####################################
#import Adafruit_DHT
 
##pin = 4
##sensor = Adafruit_DHT.DHT22
sw=8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(sw, GPIO.IN,GPIO.PUD_UP)
 
def upload_thingspeak():
    #try:
    humidity, temperature = 66,100#Adafruit_DHT.read_retry(sensor, pin)
    f = urllib.request.urlopen(url+str(humidity))
    f.read()
    f.close()
     

while True:
    sw_val=GPIO.input(sw)
    
    if sw_val== 0:
        print('k')
        upload_thingspeak()
        
        # free account has an api limit of 15sec
        time.sleep(15)



##if __name__ == "__main__":
##    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
##    while True:
##        measure(channel)
##        # free account has an api limit of 15sec
##        time.sleep(15)
