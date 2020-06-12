from RPi import GPIO

import time
import signal
import sys
#import RPi.GPIO as GPIO
from datetime import datetime

 
GPIO_BEGIN_PIN = 23
GPIO_END_PIN = 24
MAX_ALLOWED_SPEED=40
 
DISTANCE = 0.02 # (in cm) Anpassen, falls notwendig
TIMEOUT = 5 # sek
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#sending SMS to the PCR

 
if __name__ == '__main__':
    GPIO.setup(GPIO_BEGIN_PIN, GPIO.IN)
    GPIO.setup(GPIO_END_PIN, GPIO.IN)
    while 1:
        start_time, end_time = 0, 0
        
        while GPIO.input(GPIO_BEGIN_PIN) == GPIO.LOW:
            time.sleep(0.001)
            start_time = time.time()
        end_time = 0
     
        while GPIO.input(GPIO_END_PIN) == GPIO.LOW and time.time()-start_time < TIMEOUT:
            time.sleep(0.001)
        else:
            end_time = time.time()
        if(start_time!=end_time):
            speed = DISTANCE / (end_time - start_time)
            realkm = speed/27.7777777778
            if(speed>5):
                    print("Speed: %.2f cm/s" % speed)
                    print("%.2f km/h" % realkm)
                    if(speed>MAX_ALLOWED_SPEED):
                        print("te snel")