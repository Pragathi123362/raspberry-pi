import RPi.GPIO as GPIO
import time

LED=16
ir=18
sw=8
gas=22
#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(gas, GPIO.IN)
GPIO.output(LED, GPIO.LOW)

# Infinite loop
while True:
    
    gas_val=GPIO.input(gas)
    ir_val=GPIO.input(ir)
    if gas_val== 0:
        # Turn off
        GPIO.output(LED, GPIO.HIGH)
        print('Gas detected')
        time.sleep(0.5)
    elif ir_val==0:
        # Turn on
        GPIO.output(LED, GPIO.HIGH)
        print('ir detected')
        time.sleep(0.5)
def  lcd_cmd(cmd):
    
