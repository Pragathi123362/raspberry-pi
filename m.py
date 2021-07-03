import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import serial
import string
import cv2
import numpy as np
import time
import sys
import os
import smtplib
import os.path
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders






dht=Adafruit_DHT.DHT11

pin=17


soil=2
sound=25
mota=8
#motb=7
fan=1
LCD_RS=27
LCD_E=22
LCD_D4=6
LCD_D5=13
LCD_D6=19
LCD_D7=26

LCD_WIDTH=16
LCD_CHR=True
LCD_CMD=False

LCD_LINE_1=0x80
LCD_LINE_2=0xc0

E_PULSE=0.001
E_DELAY=0.001

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(soil,GPIO.IN)
GPIO.setup(sound,GPIO.IN)
GPIO.setup(mota,GPIO.OUT)
#GPIO.setup(motb,GPIO.OUT)
GPIO.setup(fan,GPIO.OUT)
GPIO.setup(LCD_RS,GPIO.OUT)
GPIO.setup(LCD_E,GPIO.OUT)
GPIO.setup(LCD_D4,GPIO.OUT)
GPIO.setup(LCD_D5,GPIO.OUT)
GPIO.setup(LCD_D6,GPIO.OUT)
GPIO.setup(LCD_D7,GPIO.OUT)


ser=serial.Serial(port='/dev/ttyAMA0',baudrate=9600,timeout=1)


while True:
    print(GPIO.input(soil))
    print("fff")
    
    if GPIO.input(soil)==0:
        print("llllll")
        msg="change the diaper"
        print("video   1")
        
       
       
        cam = cv2.VideoCapture(1)
        print("video   2")
        frame_width=int(cam.get(3))
        frame_height=int(cam.get(4))
        out=cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'),10,(frame_width,frame_height))

        print("video   3")
        for c in range(300):
            
            ret,frame=cam.read()
            cam.write(frame)

            
        email = 'pragathivijay8@gmail.com'
        password = 'Brother@4108'
        send_to_email = 'pragathivijay8@gmail.com'
        subject = 'from pibot'
        message = 'enemy detected'
        file_location = '/home/pi/Desktop/outpy.avi'
        print("loc")
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
        msg.attach(MIMEText(message, 'plain'))#attach new  message by using the Message.
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
        
    
    #time.sleep(3)
