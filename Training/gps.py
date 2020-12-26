import serial               #import serial pacakge
import time
import webbrowser           #import package for opening link in browser
import sys                  #import system package
from mcp3208 import MCP3208
import RPi.GPIO as GPIO

import smtplib
a=0
#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'ymtstraining2020@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'Ymts@Takeoff'  #change this to match your gmail password

SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


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

class Emailer:
    def sendmail(self, recipient, subject, content):
          
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit
  
sender = Emailer()
    

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    


gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

try:
    while True:
##        x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        
##
##        y = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        #print (" P1 %s " % (y))
##
##        z = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
##        #print( " P2 %s " % (z))
##        print ((" x %s " % (x)),(" y %s " % (y)),(" z %s " % (z)))
##
##        if x<1100 or x>1500 or y<1100 or y>1500:
##                print("accident Occured")
##                sendTo = 'shamlitajne96@gmail.com'
##                emailSubject = "Button Press Detected!"
##                emailContent = map_link
##                sender.sendmail(sendTo, emailSubject, emailContent)
##                print("Email Sent")


        time.sleep(2)
        
        x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        

        y = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print (" P1 %s " % (y))

        z = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print( " P2 %s " % (z))
        print ((" x %s " % (x)),(" y %s " % (y)),(" z %s " % (z)))

        if x<1100 or x>1500 or y<1100 or y>1500:
                if a==0:
                        a=1
                        received_data = (str)(ser.readline())                   #read NMEA string received
                        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
                        if (GPGGA_data_available>0):
                            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                            GPS_Info()                                          #get time, latitude, longitude
                            
        ##                    print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
        ##                    map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
        ##                    print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
        ##                    print("------------------------------------------------------------\n")
                        lat_in_degrees=str(lat_in_degrees)
                        long_in_degrees =str(long_in_degrees )
                

                        print("accident Occured")
                        map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees #create link to plot location on Google map
                        sendTo = 'shamlitajne96@gmail.com'
                        emailSubject = "Button Press Detected!"
                        emailContent = "Accident occured at"+map_link
                        sender.sendmail(sendTo, emailSubject, emailContent)
                        print("Email Sent")
        else:
                a=0
                print("safe")
                        
except KeyboardInterrupt:
    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)

