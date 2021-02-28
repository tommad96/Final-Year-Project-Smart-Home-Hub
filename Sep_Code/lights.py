import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledRed = 23
ledYellow= 24
ledGreen= 25
ledRedSts = 0
ledYellowSts = 0
ledGreenSts = 0

GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledYellow,GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYellow, GPIO.LOW)
GPIO.output(ledGreen, GPIO.LOW)

@app.route('/leds')
def index():
    ledRedSts = GPIO.input(ledRed)
    ledYellowSts = GPIO.input(ledYellow)
    ledGreenSts = GPIO.input(ledGreen)
    templateData = { 'ledRed' : ledRedSts,
    'ledYellow' : ledYellowSts,
    'ledGreen' : ledGreenSts }
    return render_template('index.html', **templateData)

@app.route('/<deviceName>/<action>')
def do(deviceName, action):
    if deviceName == "ledRed":
        actuator = ledRed
    if deviceName == "ledYellow":
        actuator = ledYellow
    if deviceName == "ledGreen":
        actuator = ledGreen
    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)
    ledRedSts = GPIO.input(ledRed)
    ledYellowSts = GPIO.input(ledYellow)
    ledGreenSts = GPIO.input(ledGreen)
    templateData = { 'ledRed' : ledRedSts,
    'ledYellow' : ledYellowSts,
    'ledGreen' : ledGreenSts }
    return render_template('index.html', **templateData )
if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
