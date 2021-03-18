import os.path
import time
#import urllib3
import sys
import urllib3
#import RPi.GPIO as GPIO
from random import *
#import adafruit_character_lcd.character_lcd as characterlcd
import os
import cv2
import numpy
import pandas as pd
from PIL import Image, ImageTk
myAPI = 'G74LQCDV9JNO73NT' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
id = 0
i=0
j=0
            # names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'GEETHA', 'ppppppppp', 'user3', 'user4', 'user5'] 

##cam = cv2.VideoCapture(0)
##
##recognizer = cv2.face.LBPHFaceRecognizer_create()
##recognizer.read('trainer.yml')
##cascadePath = "data/haarcascade_frontalface_default.xml"
##faceCascade = cv2.CascadeClassifier(cascadePath);
##
##font = cv2.FONT_HERSHEY_SIMPLEX


cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = "data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

         #iniciate id counter
  

            # Initialize and start realtime video capture
  


while True:
      ret, img =cam.read()
            #img = cv2.flip(img, -1) # Flip vertically
      gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
      faces = faceCascade.detectMultiScale(gray,1.2,5)
        ##        gray,
        ##        scaleFactor = 1.2,
        ##        minNeighbors = 5,
        ##        minSize = (int(minW), int(minH)),
        ##       )

      for(x,y,w,h) in faces:
          cv2.rectangle(img, (x,y), (x+w,y+h), (225,0,0), 2)
          id, confidence = recognizer.predict(gray[y:y+h,x:x+w])


            # Check if confidence is less them 100 ==> "0" is perfect match 
          if (confidence < 60):
              if(j==0):
                    
                    
                    print("+++++++++++++++++++++++++")
                    print(id)
                    http = urllib3.PoolManager()
                    url = baseURL +'&field1=%s' % (id)
                    print(url)
                    resp = http.request('GET', url)
                  ##            print(resp.status)
                          
                    time.sleep(2)
                    #id = list(names[id])  
                    confidence = "  {0}%".format(round(100 - confidence))
                    j=1
              if i==0:
                print(".................")
                print("Matched")
                i=1
##              if(count == 1):
##                          print('face id:',str(id),' detected')
##                            
##                          count =2
##                          i=0
##                          k=''
                                        
          else:
              id = "unknown"
              #print(id)
              print('no face detected')
              confidence = "  {0}%".format(round(100 - confidence))
              i=0
              j=0
              #time.sleep(0.1)

                
          #cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
          #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
      cv2.imshow('camera',img)
      if cv2.waitKey(100) & 0xff== ord('q'):
          break
            # Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
