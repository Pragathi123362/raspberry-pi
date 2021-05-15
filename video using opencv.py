 
import RPi.GPIO as GPIO
import cv2
import numpy
import sys
import os
import time


GPIO.setwarnings(False)

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
while(True):
    ret,img = cam.read()
##    img = cv2.flip(img, -1) # flip video image vertically
   
    cv2.imshow('/home/pi/Desktop/frame', img)

   # Press 'ESC' for exiting video
    if cv2.waitKey(100) & 0xff == ord('q'):
        break
   
#lcd_string("Your id:",LCD_LINE_1)
#lcd_byte(0x8B,LCD_CMD)
#lcd_string(str(face_id),LCD_LINE_2)
#time.sleep(2)
#lcd_byte(0x01,LCD_CMD)
# Do a bit of cleanup

cam.release()
cv2.destroyAllWindows()
