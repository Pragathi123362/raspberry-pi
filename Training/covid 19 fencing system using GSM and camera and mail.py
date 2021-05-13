import RPi.GPIO as IO
import time
from time import sleep
import cv2
import smtplib
import os
import os.path
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders
import serial
import string
import pynmea2
import os, time

#pin selection
ir1= 2
buzzer=3
ir2=4                
LCD_RS = 11
LCD_E  = 5
LCD_D4 = 6
LCD_D5 = 13
LCD_D6 = 19
LCD_D7 = 26


#pinmode
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(ir1,IO.IN)
IO.setup(buzzer,IO.OUT)
IO.setup(ir2,IO.IN)
IO.setup(LCD_E, IO.OUT)  
IO.setup(LCD_RS, IO.OUT) 
IO.setup(LCD_D4, IO.OUT) 
IO.setup(LCD_D5, IO.OUT) 
IO.setup(LCD_D6, IO.OUT) 
IO.setup(LCD_D7, IO.OUT) 

#Output set to zero
IO.output(buzzer,IO.LOW)





#Serial port enable
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


#getting gps location


# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_init():
  lcd_display(0x28,LCD_CMD) # Selecting 4 - bit mode with two rows
  lcd_display(0x0C,LCD_CMD) # Display On,Cursor Off, Blink Off
  lcd_display(0x01,LCD_CMD) # Clear display

  sleep(E_DELAY)
 
def lcd_display(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  IO.output(LCD_RS, mode) # RS
 
  # High bits
  IO.output(LCD_D4, False)
  IO.output(LCD_D5, False)
  IO.output(LCD_D6, False)
  IO.output(LCD_D7, False)
  if bits&0x10==0x10:
    IO.output(LCD_D4, True)
  if bits&0x20==0x20:
    IO.output(LCD_D5, True)
  if bits&0x40==0x40:
    IO.output(LCD_D6, True)
  if bits&0x80==0x80:
    IO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  IO.output(LCD_D4, False)
  IO.output(LCD_D5, False)
  IO.output(LCD_D6, False)
  IO.output(LCD_D7, False)
  if bits&0x01==0x01:
    IO.output(LCD_D4, True)
  if bits&0x02==0x02:
    IO.output(LCD_D5, True)
  if bits&0x04==0x04:
    IO.output(LCD_D6, True)
  if bits&0x08==0x08:
    IO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
# Toggle enable
def lcd_toggle_enable():
  time.sleep(E_DELAY)
  IO.output(LCD_E, True)
  time.sleep(E_PULSE)
  IO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
# Send string to display
def lcd_string(message,line):

 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_display(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_display(ord(message[i]),LCD_CHR)

 
lcd_init()









email = 'pragathivijay8@gmail.com'
password = 'Vijaypragathi@8'
send_to_email =  'pragathivijay8@gmail.com'
subject = 'msg from camera'
message = 'image received'
file_location = '/home/pi/Desktop/AGRI0.png'
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

#Main loop
while True:
  if IO.input(ir1)==0:
    IO.output(buzzer,IO.HIGH)
    print("Intruder- entrance")
    lcd_display(0x01,LCD_CMD)
    lcd_string("RED ZONE ALERT",LCD_LINE_1)
    time.sleep(2)
        #lcd_string("At entrance",LCD_LINE_2)
  elif IO.input(ir1)==1:
      IO.output(buzzer,IO.LOW)
      print("No Intruder-entrance")
      lcd_display(0x01,LCD_CMD)
      lcd_string("No Intruder",LCD_LINE_1)
      time.sleep(2)
      
        #lcd_string("At entrance",LCD_LINE_2)
  if IO.input(ir2)==0:
    
    camera = cv2.VideoCapture(0)
    IO.output(buzzer,IO.LOW)
    lcd_display(0x01,LCD_CMD)
    
    lcd_string("RED ZONE ALERT",LCD_LINE_1)
    time.sleep(2)
    lcd_display(0x01,LCD_CMD)
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
    lcd_string("SENDING MAIL",LCD_LINE_1)
  
 
    server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    lcd_display(0x01,LCD_CMD)
    print("mail sent")
    lcd_string("mail sent",LCD_LINE_2)
    time.sleep(2)
    lcd_display(0x01,LCD_CMD)
    server.quit()
    port.write(b'AT\r\n')
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    lcd_string("sending message",LCD_LINE_1)
    port.write(b"AT+CMGF=1\r")
    print("Text Mode Enabled…")
    time.sleep(3)
    port.write(b'AT+CMGS="9182371171"\r')
    msg = "intruder alert"
    print("sending message….")
   
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg+chr(26)))
    time.sleep(1)
    lcd_display(0x01,LCD_CMD)
    print("message sent")
    lcd_string("message sent",LCD_LINE_2)
    time.sleep(2)
    lcd_display(0x01,LCD_CMD)
         
  elif IO.input(ir2)==1:
        print("No Intruder-inside")
        IO.output(buzzer,IO.LOW)
       # lcd_string("No Intruder",LCD_LINE_1)
        #lcd_string("entered",LCD_LINE_2)
