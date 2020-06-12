import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

class DISTANCE:
    def __init__(self):
        self.trigger = 18
        self.echo = 24
        self.groen = 13
        self.geel = 19
        self.rood = 26
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.groen, GPIO.OUT)
        GPIO.setup(self.geel, GPIO.OUT)
        GPIO.setup(self.rood, GPIO.OUT)

    """ def irdetect(self):
        sensor = GPIO.input(IR)
        if(sensor==0):
            print("Sensor gedetecteerd")
            time.sleep(0.1) """

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    