import RPi.GPIO as GPIO
import time
#GPIO.cleanup()
LED=16
ir=18
sw=8
gas=22

rs=38
en=40


d4=29
d5=31
d6=33
d7=35

#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

def lcd_cmd(cmd):
    #cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.LOW)

   
    
    
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x10==0x10):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x20==0x20):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x40==0x40):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x80==0x80):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.005)

    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x02==0x02):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)
   

def lcd_data(cmd):
    cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.HIGH)
    
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)

    
    if(cmd & 0x10==0x10):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x20==0x20):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x40==0x40):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x80==0x80):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.0005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.0005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)

    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x02==0x02):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)
    

def lcd_ini():
##  lcd_cmd(0x30)
##  lcd_cmd(0x30)
##  lcd_cmd(0x30)
##  lcd_cmd(0x33)
  #lcd_cmd(0x38) 
##  lcd_cmd(0x06)
  #lcd_cmd(0x0C) 
  #lcd_cmd(0x01)

  lcd_cmd(0x33) 
  lcd_cmd(0x32) 
  lcd_cmd(0x06)
  lcd_cmd(0x0C) 
  lcd_cmd(0x28) 
  lcd_cmd(0x01) 
  time.sleep(0.0005)


def lcd_string(c):
      l=len(c)
      print(c)
      
      for i in range(l):
          lcd_data(c[i])

          
 
lcd_ini()
# Infinite loop
while True:
    lcd_cmd(0x01)
    lcd_data('k')
    lcd_string("feeling ")

    lcd_cmd(0xc0)
    lcd_string("bored")
    time.sleep(0.5)
    
    
