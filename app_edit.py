import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response
from multiprocessing import Process
from camera_pi import Camera
app = Flask(__name__)

import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledRed = 23
ledYellow= 24
ledGreen= 25
fan = 14
ledRedSts = 0
ledYellowSts = 0
ledGreenSts = 0
fanSts = 0

pirsensor_Red = 17
pirsensor_Yellow = 27
pirsensor_Green = 22
GPIO.setup(pirsensor_Red, GPIO.IN)         
GPIO.setup(pirsensor_Yellow, GPIO.IN)
GPIO.setup(pirsensor_Green, GPIO.IN)

GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledYellow,GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYellow, GPIO.LOW)
GPIO.output(ledGreen, GPIO.LOW)
GPIO.output(fan, GPIO.LOW)

DHT22Sensor = Adafruit_DHT.DHT22
DHTpin = 16

################################### LED AND FAN #################################

@app.route('/leds')
def index():
    ledRedSts = GPIO.input(ledRed)
    ledYellowSts = GPIO.input(ledYellow)
    ledGreenSts = GPIO.input(ledGreen)
    fanSts = GPIO.input(fan)
    templateData = { 'ledRed' : ledRedSts,
    'ledYellow' : ledYellowSts,
    'ledGreen' : ledGreenSts, 'fan' : fanSts}
    return render_template('index.html', **templateData)

@app.route('/<deviceName>/<action>')
def do(deviceName, action):
    if deviceName == "ledRed":
        actuator = ledRed
    if deviceName == "ledYellow":
        actuator = ledYellow
    if deviceName == "ledGreen":
        actuator = ledGreen
    if deviceName == "fan":
        actuator = fan
    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)
    ledRedSts = GPIO.input(ledRed)
    ledYellowSts = GPIO.input(ledYellow)
    ledGreenSts = GPIO.input(ledGreen)
    fanSts = GPIO.input(fan)
    templateData = { 'ledRed' : ledRedSts,
    'ledYellow' : ledYellowSts,
    'ledGreen' : ledGreenSts, 'fan' : fanSts}
    return render_template('index.html', **templateData )

############################## TEMP AND HUM SENSOR ###############################

def getDHTdata():		
	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum


@app.route("/")
def sensor():
	timeNow = time.asctime( time.localtime(time.time()) )
	temp, hum = getDHTdata()
	
	templateData = {
      'time': timeNow,
      'temp': temp,
      'hum'	: hum
	}
	return render_template('index.html', **templateData)



############################# CAMERA LIVESTREAM ####################################

@app.route('/camera')
def cam():
	"""Video streaming home page."""
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('index.html', **templateData)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

################################# PIR SENSORS #####################################
"""
def pirsensors():
    while True:
    
        if GPIO.input(pirsensor_Red) == 1:
            print("MOTION DETECTED from ledRed")
            GPIO.output(ledRed, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(ledRed, GPIO.LOW)
        elif GPIO.input(pirsensor_Yellow) == 1:
            print("MOTION DETECTED from ledYellow")
            GPIO.output(ledYellow, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(ledYellow, GPIO.LOW)
        elif GPIO.input(pirsensor_Green) == 1:
            print("MOTION DETECTED from ledGreen")
            GPIO.output(ledGreen, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(ledGreen, GPIO.LOW)
        else:
            ##print("no motion detected")
            GPIO.output(ledGreen, GPIO.LOW)
            time.sleep(2)      
pirsensors()

########################### CONTROL FAN FROM TEMP #################################

def tempfan():
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, hum))
    while True:

        if temp > 30:
           print("Temperature is at threshold FAN ON")
           GPIO.output(fan, GPIO.LOW)
           print("Fan is ON.")
           time.sleep(10)
           GPIO.output(fan,GPIO.HIGH)
           print("Fan is OFF.")
        else:
           GPIO.output(fan, GPIO.HIGH)
           print("Temperature is okay no need for fan")
tempfan()
"""
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port =  5000, debug = True, threaded = True )
    #p1 = Process(target = pirsensors)
    #p1.start()
    #p2 = process(target = tempfan)
    #p2.start()