import RPi.GPIO as GPIO
import time
import threading
from mcp3208 import MCP3208
#GPIO.cleanup()
LED=16
ir=18
sw=8
gas=22

rs=3
en=5

d0=36
d1=38
d2=40
d3=11
d4=29
d5=31
d6=33
d7=35

#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(gas, GPIO.IN)
GPIO.setup(d0, GPIO.OUT)
GPIO.setup(d1, GPIO.OUT)
GPIO.setup(d2, GPIO.OUT)
GPIO.setup(d3, GPIO.OUT)
GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)



# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)



# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(14):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout


    

def lcd_cmd(cmd):
    #cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(d0, GPIO.LOW)
    GPIO.output(d1, GPIO.LOW)
    GPIO.output(d2, GPIO.LOW)
    GPIO.output(d3, GPIO.LOW)
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
    if(cmd & 0x01==0x01):
        GPIO.output(d0, GPIO.HIGH)
    if(cmd & 0x02==0x02):
        GPIO.output(d1, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d2, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d3, GPIO.HIGH)
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
    time.sleep(0.0005)
    GPIO.output(en, GPIO.HIGH) 
   

def lcd_data(cmd):
    cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.HIGH)
    GPIO.output(d0, GPIO.LOW)
    GPIO.output(d1, GPIO.LOW)
    GPIO.output(d2, GPIO.LOW)
    GPIO.output(d3, GPIO.LOW)
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)

    if(cmd & 0x01==0x01):
        GPIO.output(d0, GPIO.HIGH)
    if(cmd & 0x02==0x02):
        GPIO.output(d1, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d2, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d3, GPIO.HIGH)
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
    time.sleep(0.0005)
    GPIO.output(en, GPIO.HIGH) 
    

def lcd_ini():
  lcd_cmd(0x30)
  lcd_cmd(0x30)
  lcd_cmd(0x30)
  lcd_cmd(0x33)
  lcd_cmd(0x38) 
  lcd_cmd(0x06)
  lcd_cmd(0x0C) 
  lcd_cmd(0x01) 
  time.sleep(0.0005)

##def lcd_string(*c):
##    i=0
##    for i in range(c[i]!='\0'):
##        lcd_data(c[i])

def lcd_string(c):
      l=len(c)
      #print(c)
      
      for i in range(l):
          lcd_data(c[i])
          
def thread_function1():
    while True:
        x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        

        y = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print (" P1 %s " % (y))

        z = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print( " P2 %s " % (z))
        print ((" x %s " % (x)),(" y %s " % (y)),(" z %s " % (z)))

        time.sleep(2)

##        pdiff = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        print (" P3 %s " % (pdiff))
##
##        pdiff = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        print (" P4 %s " % (pdiff))
##
##
##        pdiff = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        print (" P5 %s " % (pdiff))
##
##        pdiff = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        print (" P6 %s " % (pdiff))
##
##        pdiff = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        print( " P7 %s " % (pdiff))
##        GPIO.output(LED, GPIO.HIGH)
        #print("led on")
##        time.sleep(0.05)
##        GPIO.output(LED, GPIO.LOW)
       

def thread_function2():
    while True:
        gas_val=GPIO.input(gas)
        #print(gas_val)
        if gas_val== 0:
            #print('Gas detected')
            time.sleep(0.5)

def thread_function3():
    while True:
        ir_val=GPIO.input(ir)
        #print(ir_val)
        if ir_val== 0:
            #print('IR detected')
            time.sleep(0.5)
    
    
          
adc = MCP3208() 
lcd_ini()
# Infinite loop

thread1= threading.Thread(target=thread_function1)# args=(1,))

thread2= threading.Thread(target=thread_function2)

thread3= threading.Thread(target=thread_function3)


thread1.start()
thread2.start()
thread3.start()

    

while True:
    lcd_cmd(0x01)
    lcd_string("Hello")

    lcd_cmd(0xc0)
    lcd_string("world")
    time.sleep(1)





##    gas_val=GPIO.input(gas)
##    ir_val=GPIO.input(ir)
##    if gas_val== 0:
##        # Turn off
##        GPIO.output(LED, GPIO.HIGH)
##        print('Gas detected')
##        time.sleep(0.5)
##    elif ir_val==0:
##        # Turn on
##        GPIO.output(LED, GPIO.HIGH)
##        print('ir detected')
##        time.sleep(0.5)
        
