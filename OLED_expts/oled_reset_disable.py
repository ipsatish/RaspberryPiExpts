#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, getopt
pin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)
GPIO.output(pin,0)
