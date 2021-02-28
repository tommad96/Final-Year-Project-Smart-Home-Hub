import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response

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

GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledYellow,GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYellow, GPIO.LOW)
GPIO.output(ledGreen, GPIO.LOW)
GPIO.output(fan, GPIO.LOW)

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

"""
### fan test ###

@app.route('/fan')
def fans():
    fanSts = GPIO.input(fan)
    templateData = { 'fan' : fanSts }
    return render_template('index.html', **templateData)

@app.route('/<device>/<response>')
def fan(device, response ):
    if device == "fan":
        actuator = fan
    if response == "on":
        GPIO.output(actuator, GPIO.LOW)
    if response == "off":
        GPIO.output(actuator, GPIO.HIGH)
    fanSts = GPIO.input(fan)
    templateData = { 'fan' : fanSts}
    return render_template('index.html', **templateData )

### end fan test ###
"""

# get data from DHT sensor
def getDHTdata():		
	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 16
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


@app.route('/camera')
def cam():
	"""Video streaming home page."""
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('camera.html', **templateData)


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

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port =  5000, debug = True, threaded = True )