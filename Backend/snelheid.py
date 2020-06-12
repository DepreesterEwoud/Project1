from RPi import GPIO

import time
import signal
import sys
#import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO_BEGIN_PIN = 23
GPIO_END_PIN = 24
MAX_ALLOWED_SPEED=40
buzzer=20

callibrate = 0
time_for_speed = 0
velocity = 0
active = 0

GPIO.setup(GPIO_BEGIN_PIN, GPIO.IN)
GPIO.setup(GPIO_END_PIN, GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)


#GPIO.cleanup()
#sending SMS to the PCR

 
if __name__ == '__main__':
    
    while True:

        callibrate = time.time()
        #print(callibrate)
        if(GPIO.input(GPIO_BEGIN_PIN) == GPIO.LOW):
            
            while GPIO.input(GPIO_END_PIN)==GPIO.HIGH:
                time_for_speed = time.time() - callibrate
                #time.sleep(1)
                #print("eerste while")
            while GPIO.input(GPIO_END_PIN)==GPIO.LOW:
                velocity = 20/time_for_speed
                #print("tweede while")
                active = 1
        
        if(active == 1):
            print("speed")
            print("%.2f km/h" % velocity)
            if(velocity>90):
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(2) # Delay in seconds
                GPIO.output(buzzer,GPIO.LOW)
            active = 0