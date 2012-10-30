#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

PIN = 17

# set up GPIO output channel
GPIO.setup(PIN, GPIO.OUT)
# set RPi board pin 12 high
GPIO.output(PIN, GPIO.HIGH)

time.sleep(1)
