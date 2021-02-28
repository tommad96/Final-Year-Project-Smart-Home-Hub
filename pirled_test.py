import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ledRed = 23
ledYellow= 24
ledGreen= 25
pirsensor_Red = 17
pirsensor_Yellow = 27
pirsensor_Green = 22

GPIO.setup(pirsensor_Red, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(pirsensor_Yellow, GPIO.IN)
GPIO.setup(pirsensor_Green, GPIO.IN)
GPIO.setup(ledRed, GPIO.OUT)          #LED output pin
GPIO.setup(ledYellow, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)

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
            GPIO.output(ledRed, GPIO.LOW)
            GPIO.output(ledYellow, GPIO.LOW)
            GPIO.output(ledGreen, GPIO.LOW)
            time.sleep(2)      
pirsensors()
