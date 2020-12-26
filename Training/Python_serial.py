##import serial
###from serial import Serial
##
##
##if __name__ == '__main__':
##    ser = serial.Serial('ttyS0', 9600, timeout=1)
##    ser.flush()
##
##    
##    while True:
##        if ser.in_waiting > 0:
##            line = ser.readline().decode('utf-8').rstrip()
##            print(line)


import serial
from time import sleep
import codecs
a=0
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:
    received_data = ser.read()            #read serial port
    sleep(0.03)
    p=received_data.decode("utf-8")
    if p=='j':
        a=0
##    data_left = ser.inWaiting()             #check for remaining byte
##    received_data += ser.read(data_left).decode()
    #print(p)                   #print received data
    if a==0:
        a=1
        data=('received:'+p)
        print(data)
        ser.write(data.encode("utf-8"))
        sleep(2)    #transmit data serially
        
