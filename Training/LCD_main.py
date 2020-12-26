

import RPi.GPIO  as GPIO 
import time

GPIO .setwarnings(False)
GPIO .setmode(GPIO .BCM)

# Define GPIO  to LCD mapping
RS = 26
EN = 19
D4 = 13
D5 = 6
D6 = 5
D7 = 1

HIGH=1
LOW=0

GPIO .setup(RS, GPIO .OUT)
GPIO .setup(EN, GPIO .OUT)
GPIO .setup(D4, GPIO .OUT)
GPIO .setup(D5, GPIO .OUT)
GPIO .setup(D6, GPIO .OUT)
GPIO .setup(D7, GPIO .OUT)
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
 
def main():
  begin()
  lcdcmd(0x0F)
  lcdcmd(0x01)
  print("hello")
  while True:
    print("hello world")
    lcdcmd(0x01)
 
    # Send some test
    lcdprint("Electronics Hub ")
    lcdcmd(0xc0)
    lcdprint("    Presents    ")
    
    time.sleep(1) # 1 second delay
    lcdcmd(0x01)
    # Send some text
    lcdprint("Rasbperry Pi")
    lcdcmd(0xc0)
    lcdprint("16x2 LCD Test")

    time.sleep(2) # 2 second delay
    
main()
GPIO .cleanup()
##if __name__ == '__main__':
## 
##  try:
##    main()
##  except KeyboardInterrupt:
##    pass
##  finally:
##    lcdcmd(0x01)
##    GPIO .cleanup()
