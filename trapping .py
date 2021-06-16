import serial
import time
import RPi.GPIO as GPIO
from urllib.request import urlopen
import sys
import urllib3
import os
import cv2
import smtplib

import os.path
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders
import sys
import requests, json
switch=3
ir=2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

p = GPIO.PWM(21, 50)

p.start(7)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(switch, GPIO.IN,GPIO.PUD_UP)
email = 'pragathivijay8@gmail.com'
password = 'Brother@4108'
send_to_email = 'pragathivijay8@gmail.com'
subject = 'msg from camera'
message = 'location image received'
file_location = '/home/pi/Desktop/image0.png'
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


ser = serial.Serial("/dev/ttyS0",baudrate = 9600,timeout=1)


while(1):
    data=ser.readline()
    print(data)
    if data==b'\xe4':
        print("finger matched")
        time.sleep(2)
        p.ChangeDutyCycle(7) # turn towards 90 degree
        time.sleep(3) # sleep 1 second
        p.ChangeDutyCycle(2) # turn towards 0 degree
        time.sleep(1)
    elif data==b'\xe8':
        print("did not match")
    elif data==b'\xe5':
        print("no finger detected")    
    if GPIO.input(ir)==0:
        print("switch pressed")
       
        if GPIO.input(switch)==0:
            print("trap detected")
            
            p.ChangeDutyCycle(7) # turn towards 90 degree
            time.sleep(1) # sleep 1 second
            p.ChangeDutyCycle(2) # turn towards 0 degree
            time.sleep(2)
            ser.write(b'AT\r\n')
            rcv = ser.read(10)
            print(rcv)
            time.sleep(1)

            ser.write(b"AT+CMGF=1\r")
            print("Text Mode Enabled…")
            time.sleep(3)
            ser.write(b'AT+CMGS="9182371171"\r')
            h = "hello pragathi"
            print("sending message….")
            time.sleep(3)
            ser.reset_output_buffer()
            time.sleep(1)
            ser.write(str.encode(h+chr(26)))
            time.sleep(2)
            print("message sent…")
            time.sleep(1)
            print ("IMAGE UPLOADING")
            print("with in cemara")
            camera = cv2.VideoCapture(0)
            for i in range(10):
                return_value, image = camera.read()
                cv2.imwrite('image0'+str(i)+'.png', image)
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
            
            
