#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, getopt

DBG=0

def main():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        pin_arg = int(sys.argv[1])
        val = int(sys.argv[2])
	#Board GPIOs 7,11,13,15,29,31,33,35 used
        if pin_arg==0:
                pin = 7
        if pin_arg==1:
                pin = 11
        if pin_arg==2:
                pin = 13
        if pin_arg==3:
                pin = 15
        if pin_arg==4:
                pin = 29
        if pin_arg==5:
                pin = 31
        if pin_arg==6:
                pin = 33
        if pin_arg==7:
                pin = 35
	if DBG==1:
        	print 'Pin to Control is GPIO %s' % pin
        	print 'Value is %s' % val
        GPIO.setup(pin,GPIO.OUT)
        cur_val = GPIO.input(pin)
	print '%d' % cur_val
	if DBG==1:
        	print "Current value:%d" % cur_val
        if val >= 0:
                GPIO.output(pin,val)
                new_val = GPIO.input(pin)
	if DBG==1:
                print "New value:%d" % new_val
        return cur_val

if __name__ == "__main__":
        sys.exit(main())

