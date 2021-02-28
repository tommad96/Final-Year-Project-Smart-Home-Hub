"""
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

pwmOut = GPIO.PWM(14, 200)
pwmOut.start(0)

# Remember, the fan is connected to an inverter (BJT)
# so the duty cycle is the opposite ;)

dutyCycle = 0

# Main program loop

while(1):

   time.sleep(0.2)

   dutyCycle = dutyCycle + 1

 

   if(dutyCycle > 100):

       dutyCycle = 0

 

   pwmOut.ChangeDutyCycle(100 - dutyCycle)
   
   
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(14,GPIO.OUT)

while(1):

	print("Fan on")
	GPIO.output(14,GPIO.LOW)   ### as bjt in acting as an inverter high = off and low = on ###
	time.sleep(5)
	print ("Fan off")
	GPIO.output(14,GPIO.HIGH)
	time.sleep(5)
	print ("Fan on")
	GPIO.output(14,GPIO.LOW)
	print ("Fan off")
	GPIO.output(14,GPIO.HIGH)
	time.sleep(5)

