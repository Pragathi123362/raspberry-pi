
#  http://buspass.wizzie.online/
import time
from pyfingerprint.pyfingerprint import PyFingerprint
#import RPi.GPIO as gpio
import RPi.GPIO as GPIO
import sys
import urllib3
import requests
enrol=5
delet=11
inc=13
dec=15
buzzer=12
m1=16
m2=18
RS = 32
EN = 29
D4 = 31
D5 = 33
D6 = 35
D7 = 37
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(enrol, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(delet, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(inc, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(dec, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(m1, GPIO.OUT)
GPIO.setup(m2, GPIO.OUT)
GPIO.output(buzzer,GPIO.LOW)
myAPI = 'http://buspass.wizzie.online/' 
# URL where we will send the data, Don't change it
#baseURL = 'https://buspass.wizzie.online/check_status.php?' 
GPIO .setup(RS, GPIO .OUT)
GPIO .setup(EN, GPIO .OUT)
GPIO .setup(D4, GPIO .OUT)
GPIO .setup(D5, GPIO .OUT)
GPIO .setup(D6, GPIO .OUT)
GPIO .setup(D7, GPIO .OUT)

 

try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('Exception message: ' + str(e))
    exit(1)
def begin():
  lcdcmd(0x33) 
  lcdcmd(0x32) 
  lcdcmd(0x06)
  lcdcmd(0x0C) 
  lcdcmd(0x28) 
  lcdcmd(0x01) 
  time.sleep(0.0005)
 
def lcdcmd(ch): 
  GPIO .output(RS, 0)
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x10==0x10:
    GPIO .output(D4, 1)
  if ch&0x20==0x20:
    GPIO .output(D5, 1)
  if ch&0x40==0x40:
    GPIO .output(D6, 1)
  if ch&0x80==0x80:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  time.sleep(0.005)
  GPIO .output(EN, 0)
  # Low bits
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x01==0x01:
    GPIO .output(D4, 1)
  if ch&0x02==0x02:
    GPIO .output(D5, 1)
  if ch&0x04==0x04:
    GPIO .output(D6, 1)
  if ch&0x08==0x08:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  time.sleep(0.005)
  GPIO .output(EN, 0)
  
def lcdwrite(ch): 
  GPIO .output(RS, 1)
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x10==0x10:
    GPIO .output(D4, 1)
  if ch&0x20==0x20:
    GPIO .output(D5, 1)
  if ch&0x40==0x40:
    GPIO .output(D6, 1)
  if ch&0x80==0x80:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  time.sleep(0.005)
  GPIO .output(EN, 0)
  # Low bits
  GPIO .output(D4, 0)
  GPIO .output(D5, 0)
  GPIO .output(D6, 0)
  GPIO .output(D7, 0)
  if ch&0x01==0x01:
    GPIO .output(D4, 1)
  if ch&0x02==0x02:
    GPIO .output(D5, 1)
  if ch&0x04==0x04:
    GPIO .output(D6, 1)
  if ch&0x08==0x08:
    GPIO .output(D7, 1)
  GPIO .output(EN, 1)
  time.sleep(0.005)
  GPIO .output(EN, 0)
def lcdclear():
  lcdcmd(0x01)
 
def lcdprint(Str):
  l=0;
  l=len(Str)
  for i in range(l):
    lcdwrite(ord(Str[i]))
    
def setCursor(x,y):
    if y == 0:
        n=128+x
    elif y == 1:
        n=192+x
    lcdcmd(n)

##def main():
##  begin()
##  lcdcmd(0x0F)
##  lcdcmd(0x01)
##  lcdprint("Finger Did not")
##  while True:
##    print("hello world")
##    lcdcmd(0x01)
## 
##    # Send some test
##    lcdprint("Electronics Hub ")
def enrollFinger():
    
    print("Enrolling Finger")
    lcdcmd(0xc0)
           
    lcdprint("Enrolling Finger")
    time.sleep(2)
    lcdcmd(0x01)
    print('Waiting for finger...')
    
    print("Place Finger")
    lcdprint("place Finger")
    
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        
        print("Finger ALready")
        
        print("   Exists     ")
        time.sleep(2)
        return
    print('Remove finger...')
 
    print("Remove Finger")
    lcdcmd(0x01)
    lcdprint("Remove Finger")
    time.sleep(2)
    lcdcmd(0x01)
    
    print('Waiting for same finger again...')
    
    print("Place Finger")
    
    print("   Again    ")
    lcdprint("Place Finger")
    lcdcmd(0xc0)
    lcdprint("Again ")
    time.sleep(2)
    lcdcmd(0x01)
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x02)
    if ( f.compareCharacteristics() == 0 ):
        print ("Fingers do not match")
       
        print("Finger Did not")
        print("   Mactched   ")
        lcdcmd(0x01)
 
        # Send some test
        lcdprint("Finger Did not")
        lcdcmd(0xc0)
        lcdprint("    Mactched    ")
    
        time.sleep(1) # 1 second delay
        lcdcmd(0x01)
        time.sleep(2)
        return
    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print("Stored at Pos:")
    print(str(positionNumber))
    lcdprint("Finger enrolled ")
    lcdcmd(0xc0)
    lcdprint("Position:")
    lcdcmd(0xc9)
    lcdprint(str(positionNumber))
    time.sleep(2)
          
    lcdcmd(0x01)
    print("successfully")
    print('New template position #' + str(positionNumber))
    time.sleep(2)

def searchFinger():
    try:
        print('Waitingforfinger...')
        lcdcmd(0xc0)
        lcdprint("Waitingforfinger...")
        print("Waiting for finger...")
        time.sleep(2)
        lcdcmd(0x01)
        while( f.readImage() == False ):
            #pass
            time.sleep(.5)
            return
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        accuracyScore = result[1]
        if positionNumber == -1 :
            print('No match found!')
         
            print("No Match Found")
            lcdprint("No match found! ")
           
            GPIO.output(m1,GPIO.LOW)
            GPIO.output(m2,GPIO.LOW)
            GPIO.output(buzzer,GPIO.HIGH)
            print("buzzer high")
            lcdcmd(0xc0)
            lcdprint("buzzer high")
   
            time.sleep(2)
            lcdcmd(0x01)
            GPIO.output(buzzer,GPIO.LOW)
            
            return
        else:
            GPIO.output(buzzer,GPIO.LOW)
            print('Found template at position #' + str(positionNumber))
        
            print("Found at Pos:")
           
            print(str(positionNumber))
            print("finger matched")
            lcdprint("finger matched")
          
            hom = 'http://buspass.wizzie.online/check_status.php?user_id='+str(positionNumber)
            http = urllib3.PoolManager()
            resp = http.request('GET', hom)
            P=int(positionNumber)
            #r=requests.get('http://buspass.wizzie.online/check_status.php?user_id=str(positionNumber)')
            r=requests.get(hom)
##            print(hom)
##            print("xyz")
##            print(str(positionNumber))
##            print("status")
##            time.sleep(2)  
####            print(str(r.text))
            Q=str(r.text)
##            print("Q")
            
            print(Q)
            if(Q=='1'):
                
                lcdcmd(0x01)
                lcdcmd(0x0c1)
                lcdprint("gate open")
                time.sleep(2)
              
                lcdcmd(0x01)
               
               
                              
               # time.sleep(2)
                print("gate open")
                
                GPIO.output(m1,GPIO.HIGH)
                GPIO.output(m2,GPIO.LOW)
                lcdprint("gate open")
                time.sleep(2)
                lcdcmd(0x01)
                GPIO.output(m1,GPIO.LOW)
                GPIO.output(m2,GPIO.LOW)
                time.sleep(2)
                GPIO.output(m1,GPIO.LOW)
                GPIO.output(m2,GPIO.HIGH)
                time.sleep(2)
                GPIO.output(m1,GPIO.LOW)
                GPIO.output(m2,GPIO.LOW)
                lcdprint("gate close")
                print("gate close")
                time.sleep(2)
                lcdcmd(0x01)
            else:
                time.sleep(2)
                GPIO.output(buzzer,GPIO.HIGH)
                
                GPIO.output(m1,GPIO.LOW)
                GPIO.output(m2,GPIO.LOW)
                lcdcmd(0x01)
                lcdprint("fees not payed")
                print("fees not payed")
                lcdcmd(0xc0)
                lcdprint("buzzer high")
                print(str(positionNumber))
                time.sleep(2)
                GPIO.output(buzzer,GPIO.LOW)
                lcdcmd(0x01)
               
                
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
    
def deleteFinger():
    positionNumber = 0
    count=0
  
    print("Delete Finger")
    
    print("Position: ")
    print(str(count))
    lcdcmd(0x01)
    lcdprint("Delete Finger")
    lcdcmd(0xc0)
    lcdprint("Position:")
    lcdcmd(0xc9)
    lcdprint(str(count))
    time.sleep(2)
          
    lcdcmd(0x01)
   
    while GPIO.input(enrol) == True:   # here enrol key means ok
        if GPIO.input(inc) == False:
            count=count+1
            if count>1000:
                count=1000
            
            print(str(count))
            lcdcmd(0xc0)
            lcdprint("Position:")
            lcdcmd(0xc9)
            lcdprint(str(count))
            time.sleep(2)
          
            lcdcmd(0x01)
            time.sleep(0.2)
        elif GPIO.input(dec) == False:
            count=count-1
            if count<0:
                count=0
           
            print(str(count))
            lcdcmd(0xc0)
            lcdprint("Position:")
            lcdcmd(0xc9)
            lcdprint(str(count))
            time.sleep(2)
    positionNumber=count
    if f.deleteTemplate(positionNumber) == True :
        print('Template deleted!')
        
        print("Finger Deleted");
        lcdprint("Template deleted!")
        lcdcmd(0xc0)
        lcdprint("Finger Deleted")
        time.sleep(2)
        lcdcmd(0x01)



while 1:
    #gpio.output(led, HIGH)
   
    print("Place Finger")
    lcdcmd(0x01)
 
        # Send some test
    lcdprint("Place Finger")
    time.sleep(2)

    
    
    if GPIO.input(enrol) == 0:
       
        #gpio.output(led, LOW)
        enrollFinger()
    elif GPIO.input(delet) == 0:
        
       # gpio.output(led, LOW)
       # while gpio.input(delet) == 0:
        time.sleep(0.1)
        deleteFinger()
        
    else:
        searchFinger()
