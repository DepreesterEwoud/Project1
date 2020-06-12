from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from subprocess import check_output

import time
from threading import Timer

# Code voor led
from helpers.klasseknop import Button
from helpers.DISTANCE import DISTANCE
from helpers.PCF8574 import PCF8574
from RPi import GPIO
dist = DISTANCE()
GPIO.setwarnings(False)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*",engineio_logger=True)
CORS(app)
GPIO.cleanup()
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_BEGIN_PIN = 23
GPIO_END_PIN = 24
GPIO_TRIGGER_LANG_1 = 26
GPIO_ECHO_LANG_1 = 19
GPIO_ECHO_LANG_2 = 6
GPIO_TRIGGER_LANG_2 = 13
GPIO_TRIGGER_KORT = 5
GPIO_ECHO_KORT = 22
GREEN_LANG = 16
YELLOW_LANG = 12
RED_LANG = 25
GREEN_KORT = 9
YELLOW_KORT = 10
RED_KORT = 27
IR = 22
LED = 18
pin_to_circuit = 21
buzzer=20
rood_lang = True
rood_kort = True
status_licht = ""
status_licht_andere = ""
status_licht_kort = ""
status_licht_lang = ""
status_straatverlichting= ""
SDA = 2
SCL = 3
lcd_rs = 4
lcd_e = 17
callibrate = 0
time_for_speed = 0
velocity = 0
active = 0

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_BEGIN_PIN, GPIO.IN)
GPIO.setup(GPIO_END_PIN, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_LANG_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LANG_1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_LANG_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LANG_2, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_KORT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_KORT, GPIO.IN)
GPIO.setup(GREEN_LANG, GPIO.OUT)
GPIO.setup(YELLOW_LANG, GPIO.OUT)
GPIO.setup(RED_LANG, GPIO.OUT)
GPIO.setup(GREEN_KORT, GPIO.OUT)
GPIO.setup(YELLOW_KORT, GPIO.OUT)
GPIO.setup(RED_KORT, GPIO.OUT)
GPIO.setup(IR, GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

def irdetect():
    sensor = GPIO.input(IR)
    if(sensor==0):
        print("Sensor gedetecteerd")
        time.sleep(0.1)

def distance(trigger,echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def snelheid():
    global callibrate
    global time_for_speed
    global velocity
    global active

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
        active = 0

endpoint = "/api/v1"

        

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/verkeerslichten', methods=['GET'])
def get_verkeerslichten():
    if request.method == 'GET':
        s = DataRepository.read_status_lichten()
        return jsonify(status=s), 200

@app.route(endpoint + '/verkeerslichten/<verkeerslichtid>', methods=['GET'])
def get_verkeerslichtenby_id_live(verkeerslichtid):
    if request.method == 'GET':
        s = DataRepository.read_status_licht_by_id(verkeerslichtid)
        return jsonify(status=s), 200

@app.route(endpoint + '/metingen', methods=['GET'])
def get_metingen_snelheid():
    if request.method == 'GET':
        s = DataRepository.read_metingen_snelheid()
        return jsonify(status=s), 200

@app.route(endpoint + '/overtredingen', methods=['GET'])
def get_overtredingen():
    if request.method == 'GET':
        s = DataRepository.read_overtredingen()
        return jsonify(status=s), 200

# SOCKET IO
""" @socketio.on('connect')
def initial_connection():
    print('A new client connect')
    Verkeerslichtid = DataRepository.read_status_lichten()
    print(Verkeerslichtid)
    socketio.emit('B2F_switch_light', {'tbllocatie': Verkeerslichtid}) """

@socketio.on('B2F_switch_light')
def switch_light(lamp_id):
    print("Emitting data")
    data = DataRepository.read_status_licht_by_id(lamp_id)
    print(data)
    socketio.emit('B2F_switch_light', {'tbllocatie': data})

@socketio.on('F2B_verander_licht')
def switch_light(data):
    #print(data['verkeerslichtid'])
    update = DataRepository.update_status_licht(1,data['verkeerslichtid'])
    """ licht1 = DataRepository.read_status_licht_by_id(1)
    licht2 = DataRepository.read_status_licht_by_id(2)
    print(licht1) """
    #socketio.emit('B2F_switch_light', {'licht1':licht1,'licht2':licht2})


@socketio.on('F2B_verander_bijbaanlicht')
def switch_light(data):
    #print(data['verkeerslichtid'])
    update = DataRepository.update_status_licht(2,data['verkeerslichtid'])

@socketio.on('F2B_verander_straatverlichting')
def switch_light(data):
    update = DataRepository.update_status_straatverlichting(1,data['straatverlichting'])

@socketio.on('F2B_verander_autoverkeer')
def switch_light(data):
    #print(data['autoverkeerslichten'])
    update = DataRepository.update_autoverkeerslichten(1,data['autoverkeerslichten'])
    #print(update)
    """ data = DataRepository.read_status_licht_by_id(lamp_id)
    print(data)
    socketio.emit('B2F_switch_light', {'tbllocatie': data}) """
#switch_light(2)

def show_ip():
    lcd = PCF8574(SDA,SCL,0b1110000,lcd_rs,lcd_e)
    lcd.init_outputs()
    print("ip adress")
    ips = check_output(["hostname","--all-ip-addresses"])
    ips = str(ips) #een string van het ip adress maken
    ip = ips.strip("b'").split(" ") # b' weglaten en de ipadresses splitten waar een spatie staat
    print(ip[0]) #het eerste ip adress nemen van voor de spatie
    lcd.send_instruction(0x01)
    lcd.write_message(str(ip[0]))

def show_verkeerslicht():
    """ data2 = DataRepository.read_status_licht_by_id(2)
    print(data2) """ 
    global rood_kort
    global rood_lang
    global status_licht
    global status_licht_andere
    global status_licht_kort
    global status_licht_lang
    global status_straatverlichting
    #while True:
    snelheid()
    print(rc_time(pin_to_circuit))
    if(DataRepository.read_status_straatverlichting(1)['autostraatverlichting']==1):
        GPIO.output(LED, GPIO.LOW)

    if(DataRepository.read_status_straatverlichting(1)['autostraatverlichting']==2):
        GPIO.output(LED, GPIO.HIGH)
    
    if(DataRepository.read_status_straatverlichting(1)['autostraatverlichting']==3):
        if(rc_time(pin_to_circuit)>1160):
            #socketio.emit('B2F_ldrwaarde', {'ldr': rc_time(pin_to_circuit)})
            GPIO.output(LED, GPIO.HIGH)
        else:
            GPIO.output(LED, GPIO.LOW)
    """ GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.5) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW) """
    """ GPIO.output(RED_KORT,GPIO.HIGH)
    GPIO.output(YELLOW_KORT,GPIO.HIGH)
    GPIO.output(GREEN_KORT,GPIO.HIGH) """
    dist_lang_1 = distance(GPIO_TRIGGER_LANG_1, GPIO_ECHO_LANG_1)
    dist_lang_2 = distance(GPIO_TRIGGER_LANG_2, GPIO_ECHO_LANG_2)
    dist_kort = distance(GPIO_TRIGGER_KORT, GPIO_ECHO_KORT)
    print(dist_kort)
    if(DataRepository.read_autoverkeerslichten(1)['autoverkeerslichten']==1):
        if(dist_kort < 7 and dist_lang_1 < 7 or dist_lang_2 < 7):
            if(status_licht!=3 and status_licht_andere!=1):
                status_licht = 3
                status_licht_andere = 1
                DataRepository.update_status_licht(2,3)
                DataRepository.update_status_licht(1,1)
                #print("update")
                #print("Emitting data")
                licht1 = DataRepository.read_status_licht_by_id(2)
                licht2 = DataRepository.read_status_licht_by_id(1)
                #print(data)
                socketio.emit('B2F_switch_light', {'licht1': licht1, 'licht2': licht2})
                #switch_light(2)
            #print("buiten")
            #print(DataRepository.read_status_licht_by_id(2))
            if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==3 and DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==1):
                print("Niet aan het updaten")
                #Groen licht
                GPIO.output(RED_KORT,GPIO.LOW)
                GPIO.output(YELLOW_KORT,GPIO.LOW)
                GPIO.output(GREEN_KORT,GPIO.HIGH)
                GPIO.output(RED_LANG,GPIO.HIGH)
                GPIO.output(YELLOW_LANG,GPIO.LOW)
                GPIO.output(GREEN_LANG,GPIO.LOW)
                # switch_light(2)
                rood_kort = False
        else:
            if(rood_kort != True):
                #print("oranje")
                if(status_licht!=2):
                    status_licht = 2
                    DataRepository.update_status_licht(2,2)

                    licht1 = DataRepository.read_status_licht_by_id(2)
                    socketio.emit('B2F_switch_light', {'licht1': licht1})
                    #print("update")
                if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==2):
                #print(DataRepository.upate_status_licht(1,1))
                    GPIO.output(RED_KORT,GPIO.LOW)
                    GPIO.output(YELLOW_KORT,GPIO.HIGH)
                    GPIO.output(GREEN_KORT,GPIO.LOW)
                    #switch_light(2)
                    time.sleep(3)
                    rood_kort=True
            else:
                #print("rood")
                if(status_licht!=1 and status_licht_andere!=3):
                    status_licht = 1
                    status_licht_andere = 3
                    DataRepository.update_status_licht(2,1)
                    DataRepository.update_status_licht(1,3)

                    licht1 = DataRepository.read_status_licht_by_id(2)
                    licht2 = DataRepository.read_status_licht_by_id(1)
                    #print(data)
                    socketio.emit('B2F_switch_light', {'licht1': licht1, 'licht2': licht2})
                    #print("update")
                if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==1 and DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==3):
                    GPIO.output(RED_KORT,GPIO.HIGH)
                    GPIO.output(YELLOW_KORT,GPIO.LOW)
                    GPIO.output(GREEN_KORT,GPIO.LOW)
                    GPIO.output(RED_LANG,GPIO.LOW)
                    GPIO.output(YELLOW_LANG,GPIO.LOW)
                    GPIO.output(GREEN_LANG,GPIO.HIGH)
                    
                    #switch_light(2)
        if(dist_kort < 7):
            if(status_licht_kort!=3 and status_licht_lang!=1):
                status_licht_kort = 3
                status_licht_lang = 1
                DataRepository.update_status_licht(2,3)
                DataRepository.update_status_licht(1,1)

                licht1 = DataRepository.read_status_licht_by_id(2)
                licht2 = DataRepository.read_status_licht_by_id(1)
                #print(data)
                socketio.emit('B2F_switch_light', {'licht1': licht1, 'licht2': licht2})
                print("update")
                #switch_light(2)
            #print("buiten")
            #print(DataRepository.read_status_licht_by_id(2))
            if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==3 and DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==1):
                print("Niet aan het updaten")
                #Groen licht
                GPIO.output(RED_KORT,GPIO.LOW)
                GPIO.output(YELLOW_KORT,GPIO.LOW)
                GPIO.output(GREEN_KORT,GPIO.HIGH)
                GPIO.output(RED_LANG,GPIO.HIGH)
                GPIO.output(YELLOW_LANG,GPIO.LOW)
                GPIO.output(GREEN_LANG,GPIO.LOW)
                # switch_light(2)
                rood_lang = False
        else:
            if(rood_lang != True):
                #print("oranje")
                if(status_licht_kort!=2):
                    status_licht_kort = 2
                    DataRepository.update_status_licht(2,2)
                    #print("update")
                if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==2):
                #print(DataRepository.upate_status_licht(1,1))
                    GPIO.output(RED_KORT,GPIO.LOW)
                    GPIO.output(YELLOW_KORT,GPIO.HIGH)
                    GPIO.output(GREEN_KORT,GPIO.LOW)
                    #switch_light(2)
                    time.sleep(3)
                    rood_lang=True
            else:
                #print("rood")
                if(status_licht_kort!=1 and status_licht_lang!=3):
                    status_licht_kort = 1
                    status_licht_lang = 3
                    DataRepository.update_status_licht(2,1)
                    DataRepository.update_status_licht(1,3)

                    licht1 = DataRepository.read_status_licht_by_id(2)
                    licht2 = DataRepository.read_status_licht_by_id(1)
                    #print(data)
                    socketio.emit('B2F_switch_light', {'licht1': licht1, 'licht2': licht2})
                    #print("update")
                if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==1 and DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==3):
                    GPIO.output(RED_KORT,GPIO.HIGH)
                    GPIO.output(YELLOW_KORT,GPIO.LOW)
                    GPIO.output(GREEN_KORT,GPIO.LOW)
                    GPIO.output(RED_LANG,GPIO.LOW)
                    GPIO.output(YELLOW_LANG,GPIO.LOW)
                    GPIO.output(GREEN_LANG,GPIO.HIGH)
    else:
        if(DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==1):
            GPIO.output(RED_LANG,GPIO.HIGH)
            GPIO.output(YELLOW_LANG,GPIO.LOW)
            GPIO.output(GREEN_LANG,GPIO.LOW)

        if(DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==2):
            GPIO.output(RED_LANG,GPIO.LOW)
            GPIO.output(YELLOW_LANG,GPIO.HIGH)
            GPIO.output(GREEN_LANG,GPIO.LOW)

        if(DataRepository.read_status_licht_by_id(1)['verkeerslichtid']==3):
            GPIO.output(RED_LANG,GPIO.LOW)
            GPIO.output(YELLOW_LANG,GPIO.LOW)
            GPIO.output(GREEN_LANG,GPIO.HIGH)

        if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==1):
            GPIO.output(RED_KORT,GPIO.HIGH)
            GPIO.output(YELLOW_KORT,GPIO.LOW)
            GPIO.output(GREEN_KORT,GPIO.LOW)

        if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==2):
            GPIO.output(RED_KORT,GPIO.LOW)
            GPIO.output(YELLOW_KORT,GPIO.HIGH)
            GPIO.output(GREEN_KORT,GPIO.LOW)

        if(DataRepository.read_status_licht_by_id(2)['verkeerslichtid']==3):
            GPIO.output(RED_KORT,GPIO.LOW)
            GPIO.output(YELLOW_KORT,GPIO.LOW)
            GPIO.output(GREEN_KORT,GPIO.HIGH)
        
        #rint ("Measured Distance = %.1f cm" % dist_lang_1)
        #time.sleep(1)"""
    """ data = DataRepository.read_status_licht_by_id(2)
    print(data)  """
    Timer(1,show_verkeerslicht).start()
#show_ip()
show_verkeerslicht()
#Timer(1, show_verkeerslicht).start()

if __name__ == '__main__':
    #print("test binnen main")
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    #print("test na socketio")
    