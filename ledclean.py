#defining the RPi's pins as Input / Output
import RPi.GPIO as GPIO

#used for GPIO numbering
GPIO.setmode(GPIO.BCM)
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

#cleaning up GPIO states and shutting off LED
GPIO.cleanup()
