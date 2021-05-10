import RPi.GPIO as GPIO

import time
from urllib.request import urlopen
import sys
import Adafruit_DHT
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
import sys
import requests, json
  
# Enter your API key here
api_key = "d4d8c6405ab3a1bb82d107739b1db63b"
  
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  

pin=4
i=0
j=0
k=0
switch=26
ir=17
relay1=3
relay2=2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ir, GPIO.IN)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(switch, GPIO.IN,GPIO.PUD_UP)
GPIO.output(relay1,0)
GPIO.output(relay2,0)
GPIO.setup(pin,GPIO.OUT)















email = 'pragathivijay8@gmail.com'
password = 'Vijaypragathi@8'
send_to_email = 'jijumol.babu75@gmail.com'
subject = 'msg from camera'
message = 'location image received'
file_location = '/home/pi/AGRI0.png'
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



try:
    while True:
         # print(GPIO.input(ir) )
         
        if GPIO.input(ir) == 0:
            GPIO.output(relay1,1)
           
        else:
            GPIO.output(relay1,0)
        city_name = "tirupati"
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)   
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            temperature=current_temperature-273.15
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            print("temperature :"+str(temperature))
           
            print("atmospheric pressure :" +str(current_pressure))
           
            print("humidity :"+str(current_humidity)) 
          
          
        else:
            print(" City Not Found ")
       
        # complete url address
            
          
        # get method of requests module
        # return response object
            
          
        # json method of response object 
        # convert json format data into
        # python format data
           
          
        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found
            
          
            # store the value corresponding
            # to the "temp" key of y
               
            
           
            # store the value corresponding
            # to the "pressure" key of y
                
          
            # store the value corresponding
            # to the "humidity" key of y
                
          
            # store the value of "weather"
            # key in variable z
               
          
            # store the value corresponding 
            # to the "description" key at 
            # the 0th index of z
               
          
            # print following values
                

        
        humidity, Temperature = Adafruit_DHT.read_retry(11,pin)
        
        tem=str(Temperature)
        
##        print("temp"  ,temperature)
       
        if GPIO.input(switch) == 0:
            print("switch pressed")
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
            i=0
            # city_name = input("Enter city name : ")
           
##        if GPIO.input(switch) == 1:
##            print("switch not pressed")
##            i=1
       
           
            
        if Temperature> 39:
##            print("temperature high")
            GPIO.output(relay2,1)
           
        else:
##            print("normal temperature")
            GPIO.output(relay2,0)
           
            
        
            
        
                    



except KeyboardInterrupt:
    print("Quit")

# Reset GPIO settings
GPIO.cleanup()
