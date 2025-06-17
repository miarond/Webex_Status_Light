#!/usr/bin/python
# 2020-12-22 Aron Donaldson
# Webex Status Light - Improved by Aron Donaldson, original concept from:
# 2020-04-01 Matthew Fugel, https://github.com/matthewf01/Webex-Teams-Status-Box
# Example wiring diagrams for LEDs
# https://www.instructables.com/id/Raspberry-Pi-3-RGB-LED-With-Using-PWM/

import os
import time
import sys
from webexpythonsdk import WebexAPI, ApiError, RateLimitError
import RPi.GPIO as GPIO

# Obtaining Bot token and PersonID from environmental variables
bot_token=os.environ.get('BOT_ACCESS_TOKEN')
api=WebexAPI(access_token=bot_token)
mywebexid=os.environ.get('PERSON_ID')

# Helpful stuff you can run if using your personal access token temporarily to test:
# person= api.people.me()
# print(person.status,person.displayName)

# Set up for RGB LEDs. Use GPIO pins referenced below when wiring:
# By using BCM mode the module uses pinout numbers as they are assigned by the Broadcom SOC. This method could cause the script to fail if hardware revisions change the pin layout in the future.
GPIO.setmode(GPIO.BCM)
green=11
red=9
yellow=10
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
freq=100 #for PWM control
RED=GPIO.PWM(red, freq)
GREEN=GPIO.PWM(green, freq)
YELLOW=GPIO.PWM(yellow, freq)

# Variable to capture last active color
last_state=None

# Create function to turn light on
def led_on(color):
	if color == "RED":
		RED.ChangeDutyCycle(100)
	elif color == "YELLOW":
		YELLOW.ChangeDutyCycle(100)
	else:
		GREEN.ChangeDutyCycle(100)

# Create function to turn light off
def led_off(color=None):
		if color:
			color.ChangeDutyCycle(0)
		else:
			for color in ("RED", "YELLOW", "GREEN"):
				color.ChangeDutyCycle(0)

# Start the GPIO pin output like a drag strip light tree :)
RED.start(100)
time.sleep(1)
YELLOW.start(100)
time.sleep(1)
GREEN.start(100)
time.sleep(1)
led_off("RED")
led_off("YELLOW")
led_off("GREEN")

while True:
	try:
		status = api.people.get(personId=mywebexid).status
		#Status codes include: active,inactive,DoNotDisturb,meeting,presenting,call
		led_off(last_state)
		if status in ("active", "inactive"):
			print("Status is:", status, "Action: GREEN")
			led_on("GREEN")
			last_state = "GREEN"
			time.sleep(15)
		elif status in ("call", "meeting"):
			print("Status is:", status, "Action: YELLOW")
			led_on("YELLOW")
			last_state = "YELLOW"
			time.sleep(15)
		elif status in ("OutOfOffice"):
			print("Status is:", status, "Action: OFF")
			led_off(last_state)
			last_state = None
			time.sleep(300)
		else:
			print("Status is:", status, "Action: RED")
			led_on("RED")
			last_state = "RED"
			time.sleep(15)
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit(0)
	except ApiError as e:
		print("Unexpected error occured:",e)
		time.sleep(5)
	except RateLimitError as e:
		print(f"Rate limit reached; backing off {e.retry_after} seconds.")
		time.sleep(e.retry_after)
	except:
		time.sleep(5)
