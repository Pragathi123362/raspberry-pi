import RPi.GPIO as GPIO
import cv2
import numpy
import sys
import os
import time

from PIL import Image, ImageTk 
import pandas as pd 
##from pyfingerprint.pyfingerprint import PyFingerprint
##import serial
####LCD_RS=17
##LCD_E=27
##LCD_D4=6
##LCD_D5=13
##LCD_D6=19
##LCD_D7=26

##LCD_WIDTH=16
##LCD_CHR= True
##LCD_CMD= False

##LCD_LINE_1 = 0x80
##LCD_LINE_2 = 0xc0

##E_PULSE = 0.001
##E_DELAY = 0.001
##def lcd_init():
##    lcd_byte(0x33,LCD_CMD)
##    lcd_byte(0x32,LCD_CMD)
##    lcd_byte(0x06,LCD_CMD)
##    lcd_byte(0x0c,LCD_CMD)
##    lcd_byte(0x28,LCD_CMD)
##    lcd_byte(0x01,LCD_CMD)
##    time.sleep(E_DELAY)
##
##def lcd_byte(bits,mode):
##    GPIO.output(LCD_RS,mode)
##    GPIO.output(LCD_D4,False)
##    GPIO.output(LCD_D5,False)
##    GPIO.output(LCD_D6,False)
##    GPIO.output(LCD_D7,False)
##    if bits&0x10==0x10:
##        GPIO.output(LCD_D4,True)
##    if bits&0x20==0x20:
##        GPIO.output(LCD_D5,True)
##    if bits&0x40==0x40:
##        GPIO.output(LCD_D6,True)
##    if bits&0x80==0x80:
##        GPIO.output(LCD_D7,True)
##    lcd_toggle_enable()
##
##    GPIO.output(LCD_D4,False)
##    GPIO.output(LCD_D5,False)
##    GPIO.output(LCD_D6,False)
##    GPIO.output(LCD_D7,False)
##    if bits&0x01==0x01:
##        GPIO.output(LCD_D4,True)
##    if bits&0x02==0x02:
##        GPIO.output(LCD_D5,True)
##    if bits&0x04==0x04:
##        GPIO.output(LCD_D6,True)
##    if bits&0x08==0x08:
##        GPIO.output(LCD_D7,True)
##
##    lcd_toggle_enable()
##
##def lcd_toggle_enable():
##    time.sleep(E_DELAY)
##    GPIO.output(LCD_E,True)
##    time.sleep(E_PULSE)
##    GPIO.output(LCD_E,False)
##    time.sleep(E_DELAY)
##
##def lcd_string(message,line):
##    message=message.ljust(LCD_WIDTH," ")
##    lcd_byte(line,LCD_CMD)
##    for i in range(LCD_WIDTH):
##        lcd_byte(ord(message[i]),LCD_CHR)
GPIO.setwarnings(False)
##GPIO.setmode(GPIO.BCM)
##GPIO.setup(LCD_E, GPIO.OUT)
##GPIO.setup(LCD_RS,GPIO.OUT)
##GPIO.setup(LCD_D4,GPIO.OUT)
##GPIO.setup(LCD_D5,GPIO.OUT)
##GPIO.setup(LCD_D6,GPIO.OUT)
##GPIO.setup(LCD_D7,GPIO.OUT)
##lcd_init()
##try:
##    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
##
##    if ( f.verifyPassword() == False ):
##        raise ValueError('The given fingerprint sensor password is wrong!')
##except Exception as e:
##    print('The fingerprint sensor could not be initialized!')
##    print('Exception message: ' + str(e))
##    exit(1)
##print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
##try:
##    #print('Waiting for finger...')
##    #lcd_string("Place your thumb",LCD_LINE_1)
##
##    ## Wait that finger is read
##    while ( f.readImage() == False ):
##        pass
##
##    ## Converts read image to characteristics and stores it in charbuffer 1
##    f.convertImage(0x01)
##
##    ## Checks if finger is already enrolled
##    result = f.searchTemplate()
##    positionNumber = result[0]
##
##    if ( positionNumber >= 0 ):
##        print('Template already exists at position #' + str(positionNumber))
##        exit(1)
##
##    #print('Remove finger...')
##    time.sleep(2)
##
##    #print('Waiting for same finger again...')
##
##    ## Wait that finger is read again
##    while ( f.readImage() == False ):
##        pass
##
##    ## Converts read image to characteristics and stores it in charbuffer 2
##    f.convertImage(0x02)
##
##    ## Compares the charbuffers
##    if ( f.compareCharacteristics() == 0 ):
##        raise Exception('Fingers do not match')
##
##    ## Creates a template
##    f.createTemplate()
##
##    ## Saves template at new position number
##    positionNumber = f.storeTemplate()
##    print('Finger enrolled successfully!')
##    print('New template position #' + str(positionNumber))
##   # lcd_string("Finger enrolled",LCD_LINE_1)
##except Exception as e:
##    print('Operation failed!')
##    print('Exception message: ' + str(e))
##    exit(1)
cam = cv2.VideoCapture(0)
#cam.set(3, 640) # set video width
#cam.set(4, 480) # set video height
harcascadePath = "data/haarcascade_frontalface_default.xml"
#face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
detector = cv2.CascadeClassifier(harcascadePath)
# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
#lcd_string("Look at camera",LCD_LINE_1)
# Initialize individual sampling face count
count = 0

while(True):
    ret,img = cam.read()
##    img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.5, 5)
    #faces = face_detector.detectMultiScale(gray)
    #faces = face_detector.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

    cv2.imshow('image', img)

   # Press 'ESC' for exiting video
    if cv2.waitKey(100) & 0xff == ord('q'):
        break
    elif count >= 80: # Take 30 face sample and stop video
         break
#lcd_string("Your id:",LCD_LINE_1)
#lcd_byte(0x8B,LCD_CMD)
#lcd_string(str(face_id),LCD_LINE_2)
#time.sleep(2)
#lcd_byte(0x01,LCD_CMD)
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
