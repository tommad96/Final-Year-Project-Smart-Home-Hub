import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

fan = 14
GPIO.setup(fan, GPIO.OUT)

DHT22Sensor = Adafruit_DHT.DHT22
DHTpin = 16

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
        #else:
           #GPIO.output(fan, GPIO.HIGH)
           #print("Temperature is okay no need for fan")
tempfan()

