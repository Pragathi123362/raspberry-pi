import RPi.GPIO as GPIO
import time
import threading
from urllib.request import urlopen
import sys
import urllib3
import os

BASE_URL = "http://embparking.wizzie.online/spot_booking.php?"

#GPIO.cleanup()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18
TRIG1 = 7
ECHO1 = 8
TRIG2 = 13
ECHO2 = 10
TRIG3 = 11
ECHO3 = 12
Rled=38
Gled=40
Rled1=32
Gled1=36
Rled2=22
Gled2=24
Rled3=26
Gled3=29
i=0
j=0
k=0
l=0
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG3,GPIO.OUT)
GPIO.setup(ECHO3,GPIO.IN)
GPIO.setup(Rled,GPIO.OUT)
GPIO.setup(Gled,GPIO.OUT)
GPIO.setup(Rled1,GPIO.OUT)
GPIO.setup(Gled1,GPIO.OUT)
GPIO.setup(Rled2,GPIO.OUT)
GPIO.setup(Gled2,GPIO.OUT)
GPIO.setup(Rled3,GPIO.OUT)
GPIO.setup(Gled3,GPIO.OUT)
GPIO.output(TRIG, False)
GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)
GPIO.output(Rled, GPIO.LOW)
GPIO.output(Gled, GPIO.LOW)
print("Calibrating.....")
time.sleep(2)

print("Place the object......")
          
def thread_function1():
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance+1.15, 2)
        if distance<=10 and distance>=5:
           print("object")
           GPIO.output(Rled, GPIO.HIGH)
           GPIO.output(Gled, GPIO.LOW)
           hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'1''&id='+'1'
           http = urllib3.PoolManager()
           resp = http.request('GET', hom)
           print(resp.status)
           print(hom)
        
           print("sent")
##           print("Response: {}".format(conn.read()))
##           conn.close()
       
           i=1
        else:
            print("no object....")
            GPIO.output(Gled, GPIO.HIGH)
            GPIO.output(Rled, GPIO.LOW)
            hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'0''&id='+'1'
            http = urllib3.PoolManager()
            resp = http.request('GET', hom)
            print(resp.status)
            print(hom)
        
            print("sent")
##            print("Response: {}".format(conn.read()))
##            conn.close()
       
            i=0
        time.sleep(2)        
def thread_function2():
    while True:
        GPIO.output(TRIG1, True)
        time.sleep(0.00001)
        GPIO.output(TRIG1, False)
        while GPIO.input(ECHO1)==0:
           pulse_start1 = time.time()

        while GPIO.input(ECHO1)==1:
           pulse_end1 = time.time()
        pulse_duration1 = pulse_end1 - pulse_start1

        distance1 = pulse_duration1* 17150
     
        distance1 = round(distance1+1.15, 2)
        if distance1<=10 and distance1>=5:
           print("object1")
           GPIO.output(Rled1, GPIO.HIGH)
           GPIO.output(Gled1, GPIO.LOW)
           hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'1''&id='+'2'
           http = urllib3.PoolManager()
           resp = http.request('GET', hom)
           print(resp.status)
           print(hom)
        
           print("sent")
##           print("Response: {}".format(conn.read()))
##           conn.close()
       
           i=1
        else:
            print("no object....")
            GPIO.output(Gled1, GPIO.HIGH)
            GPIO.output(Rled1, GPIO.LOW)
            hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'0''&id='+'2'
            http = urllib3.PoolManager()
            resp = http.request('GET', hom)
            print(resp.status)
            print(hom)
        
            print("sent")
##            print("Response: {}".format(conn.read()))
##            conn.close()
            i=0
        time.sleep(2)        
def thread_function3():
    while True:
        GPIO.output(TRIG2, True)
        time.sleep(0.00001)
        GPIO.output(TRIG2, False)
        while GPIO.input(ECHO2)==0:
            pulse_start2 = time.time()

        while GPIO.input(ECHO2)==1:
            pulse_end2 = time.time()
        pulse_duration2 = pulse_end2 - pulse_start2

        distance2 = pulse_duration2* 17150
     
        distance2 = round(distance2+1.15, 2)
        if distance2<=10 and distance2>=5:
           print("object2")
           hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'1'+'&id='+'3'
           http = urllib3.PoolManager()
           resp = http.request('GET', hom)
           print(resp.status)
           print(hom)
            
           print("sent")
##           print("Response: {}".format(conn.read()))
##           conn.close()
           
           GPIO.output(Rled2, GPIO.HIGH)
           GPIO.output(Gled2, GPIO.LOW)
           i=1
        else:
            print("no object....")
            GPIO.output(Gled2, GPIO.HIGH)
            GPIO.output(Rled2, GPIO.LOW)
            hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'0''&id='+'3'
            http = urllib3.PoolManager()
            resp = http.request('GET', hom)
            print(resp.status)
            print(hom)
        
            print("sent")
##            print("Response: {}".format(conn.read()))
##            conn.close()
       
            i=0
        time.sleep(2)        
def thread_function4():
    while True:
        GPIO.output(TRIG3, True)
        time.sleep(0.00001)
        GPIO.output(TRIG3, False)
        while GPIO.input(ECHO3)==0:
            pulse_start3 = time.time()

        while GPIO.input(ECHO3)==1:
            pulse_end3 = time.time()     
          
        pulse_duration3 = pulse_end3 - pulse_start3

        distance3 = pulse_duration3* 17150
     
        distance3 = round(distance3+1.15, 2)
        if distance3<=10 and distance3>=5:
           print("object3")
           GPIO.output(Rled3, GPIO.HIGH)
           GPIO.output(Gled3, GPIO.LOW)
           hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'1'+'&id='+'4'
           http = urllib3.PoolManager()
           resp = http.request('GET', hom)
           print(resp.status)
           print(hom)
        
           print("sent")
##           print("Response: {}".format(conn.read()))
##           conn.close()
       
           i=1
        else:
            print("no object....")
            GPIO.output(Gled3, GPIO.HIGH)
            GPIO.output(Rled3, GPIO.LOW)
            hom = 'http://embparking.wizzie.online/spot_booking.php?s='+'0'+'&id='+'4'
            http = urllib3.PoolManager()
            resp = http.request('GET', hom)
            print(resp.status)
            print(hom)
        
            print("sent")
##            print("Response: {}".format(conn.read()))
##            conn.close()
       
            i=0
        time.sleep(2)    
thread1= threading.Thread(target=thread_function1)# args=(1,))

thread2= threading.Thread(target=thread_function2)

thread3= threading.Thread(target=thread_function3)

thread4= threading.Thread(target=thread_function4)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
