


#working

import blynklib
import RPi.GPIO as GPIO
import blynklib
import time
from urllib.request import urlopen
import sys
import Adafruit_DHT as dht
import urllib3
import os
import cv2
import smtplib
from Adafruit_IO import Client, Feed, RequestError
import os.path
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders




m11=8
m12=10
m21=12
m22=16
dt=18
moisture=15
rain=18
##weeder=23
##pump=16

import sys
import RPi.GPIO as IO # Import Raspberry Pi GPIO libraryfrom Adafruit_IO import Client, Feed
import time
from time import sleep
import serial
from mcp3208 import MCP3208

IO.setwarnings(False)
IO.setmode(IO.BOARD)

SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24
IO.setup(SPIMOSI, IO.OUT)
IO.setup(SPIMISO, IO.IN)
IO.setup(SPICLK, IO.OUT)
IO.setup(SPICS, IO.OUT)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(rain, GPIO.IN)
##GPIO.setup(weeder, GPIO.OUT)
##GPIO.setup(pump, GPIO.OUT)

GPIO.setup(dt, GPIO.IN)
GPIO.setup(moisture, GPIO.IN)





#sensor=Adafruit_DHT.DHT11

GPIO.output(m11 , 0)
GPIO.output(m12 , 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)



BASE_URL = "http://embagribot.wizzie.online/save_values.php?"







email = 'pragathivijay8@gmail.com'
password = 'Vijaypragathi@8'
send_to_email = 'pragathivijay8@gmail.com'
subject = 'msg from agribot'
message = 'location image received'
file_location = '/home/pi/Downloads/agribot/mcp3208-master/AGRI0.png'
msg = MIMEMultipart()#Create the container (outer) email message.
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject
'''as.string() 
|
+------------MIMEMultipart 
              |                                                |---content-type 
              |                                   +---header---+---content disposition 
              +----.attach()-----+----MIMEBase----| 
                                 |                +---payload (to be encoded in Base64)
                                 +----MIMEText'''
msg.attach(MIMEText(message, 'plain'))#attach new  message by using the Message.attach

auth_token = 'BRD1TgbbDtZLdZRNIo56BVRNkEpGB7O-'


# Initialize Blynk

blynk = blynklib.Blynk(auth_token)
@blynk.handle_event('write V0')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo =="1":
        print ("LEFT")
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 1)
        GPIO.output(m12 , 0)
    else:
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
    
@blynk.handle_event('write V1')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo =="1":
        print ("RIGHT")
        GPIO.output(m21 , 1)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
    else:
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
        

        
@blynk.handle_event('write V2')
def write_handler_pin_handler(pin, value):
    Doorlock = (format(value[0]))
    if Doorlock =="1":
        print ("STOP")
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)

        
@blynk.handle_event('write V3')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo  =="1":
        print ("FORWARD")
        GPIO.output(m21 , 1)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 1)
        GPIO.output(m12 , 0)

@blynk.handle_event('write V4')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo =="1":
        print ("BACK")
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 1)
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 1)
    else:
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
@blynk.handle_event('write V5')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo =="1":
        GPIO.output(m11 , 0)
        GPIO.output(m12 , 0)
        GPIO.output(m21 , 0)
        GPIO.output(m22 , 0)
        x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print("raindrop: " ,x)
    

        y= readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print("moisture: " ,y);
        z=x/1000
        a=y/1000
        humi, temp = DHT11_data()
##        print("reading");
        print("Humidity= ",humi)
        print("Temperature = ",temp)##
##        humidity, temperature = Adafruit_DHT.read_retry(sensor,dt )
##        water=GPIO.input(moisture)
####        raindrop=GPIO.input(rain)
####        s=raindrop
####        soil=water
####        r=raindrop
##        y = int(temperature)
##        x = int(humidity)
####        z = int(water)
####        a=int(r)
####
        print(' rain={1:0.1f}%   moisture={1:0.1f}%'.format(z,a))
####        soil=waters=raindrop
####        soil=water))
##            
##        print("MOISTURE VALUE(I.E DRY=1,WET=0)=",water)
####    
####        print("rain VALUE(I.E DRY=1,WET=0)=",s)
####        soil=water
####
##        hom = 'http://embagribot.dbandroid.online/save_values.php?'+'tmp='+str(y)+'&&humidity='+ str(x)+'&&soil='+str(z)+'&&id=user1'
##        http = urllib3.PoolManager()
##        resp = http.request('GET', hom)
##        print(resp.status)
##        print(hom)
##        
##        print("sent")
##        print("Response: {}".format(conn.read()))
####        conn.close()
##
@blynk.handle_event('write V6')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo =="1":
        print ("IMAGE UPLOADING")
        print("with in cemara")
        camera = cv2.VideoCapture(0)
        for i in range(10):
            return_value, image = camera.read()
            cv2.imwrite('AGRI'+str(i)+'.png', image)
            print('AGRI IMG captured')
            time.sleep(2)
            break
        del(camera)
        
        
        filename = os.path.basename(file_location)#function returns the tail of the path
        attachment = open(file_location, "rb") #“rb” (read binary)
        part = MIMEBase('application', 'octet-stream')#Content-Type: application/octet-stream , image/png, application/pdf
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)#Content-Disposition: attachment; filename="takeoff.png"
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)# Send the message via local SMTP server.
        print("SENDING MAIL")
        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        print("mail sent")
        server.quit()
@blynk.handle_event('write V7')
def write_handler_pin_handler(pin, value):
    robo = (format(value[0]))
    if robo =="1":
        print ("pump ON")
        GPIO.output(pump , 1)
    else:
        print ("pump OFF")
        GPIO.output(pump , 0)
        


@blynk.handle_event('write V9')
def write_handler_pin_handler(pin, value):
    robo  = (format(value[0]))
    if robo =="1":
        print ("seder ON")
        GPIO.output(seeder , 1)
    else:
        print ("seder OFF")
        GPIO.output(seeder , 0)
def DHT11_data():
    
	# Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT11, 18)
##    print("Humidity= ",humi)
##    print("Temperature = ",temp)
    return humi, temp
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
          
    
    if ((adcnum > 7) or (adcnum < 0)):
                           
        
        return -1
    IO.output(cspin, True)

    IO.output(clockpin, False)  # start clock low
    IO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
                                                      
            IO.output(mosipin, True)
        else:
            IO.output(mosipin, False)
        commandout <<= 1
        IO.output(clockpin, True)
        IO.output(clockpin, False)

    adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
    for i in range(14):
        IO.output(clockpin, True)
        IO.output(clockpin, False)
        adcout <<= 1
        if (IO.input(misopin)):
            adcout |= 0x1

    IO.output(cspin, True)
        
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout


while True:
    
    blynk.run()
    
        
                    
 
##except KeyboardInterrupt:
##    print("Quit")
##
### Reset GPIO settings
##GPIO.cleanup()
##    time.sleep(1)
##    
##time.sleep(2)
