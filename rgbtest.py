#defining the RPi's pins as Input / Output
import RPi.GPIO as GPIO

#importing the library for delaying command.
import time

#used for GPIO numbering
GPIO.setmode(GPIO.BCM)

#closing the warnings when you are compiling the code
GPIO.setwarnings(False)

RUNNING = True

#defining the pins
green = 11
red = 9
yellow = 10

#defining the pins as output
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)

#choosing a frequency for pwm
Freq = 100

#defining the pins that are going to be used with PWM
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
YELLOW = GPIO.PWM(yellow, Freq)

try:
	#we are starting with the loop
	while RUNNING:
		#lighting up the pins. 100 means giving 100% to the pin
		#RED.start(100)
		#GREEN.start(100)
		#YELLOW.start(100)
		#For anode RGB LED users, the duty cycle is inverse from cathod LEDs.  A lower value increases brightness and a higher value decreases brightness.

		# for changing the width of PWM, this command is used
		RED.start(100)
		time.sleep(1)
		RED.stop()
		YELLOW.start(100)
		time.sleep(1)
		YELLOW.stop()
		GREEN.start(100)
		time.sleep(1)
		GREEN.stop()
		# The sub-module "ChangeDutyCycle()" allows you to change the power output without stopping and starting the LED.
		#RED.ChangeDutyCycle(0)
		#YELLOW.ChangeDutyCycle(0)
		#GREEN.ChangeDutyCycle(0)
		time.sleep(1)

except KeyboardInterrupt:
	# the purpose of this part is, when you interrupt the code, it will stop the while loop and turn off the pins, which means your LED won't light anymore
	RUNNING = False
	GPIO.cleanup()
