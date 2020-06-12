import time
import serial
from RPi import GPIO
from subprocess import check_output
from helpers.PCF8574 import PCF8574
GPIO.setwarnings(False)
SDA = 2
SCL = 3
lcd_rs = 4
lcd_e = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
if __name__ == "__main__":
    GPIO.cleanup()
    try:
        GPIO.cleanup()
        lcd = PCF8574(SDA,SCL,0b1110000,lcd_rs,lcd_e)
        lcd.init_outputs()
        print("ip adress")
        ips = check_output(["hostname","--all-ip-addresses"])
        ips = str(ips) #een string van het ip adress maken
        ip = ips.strip("b'").split(" ") # b' weglaten en de ipadresses splitten waar een spatie staat
        print(ip[0]) #het eerste ip adress nemen van voor de spatie
        lcd.send_instruction(0x01)
        lcd.write_message(str(ip[0]))
        #(while(True):
            
 
    except KeyboardInterrupt as e:
        print("quitting...")
       
    finally:
        #mcp.close_spi()
        GPIO.cleanup()