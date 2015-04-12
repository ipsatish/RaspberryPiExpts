#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, getopt

DBG=0

def main():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pin_arg = int(sys.argv[1])
        val = int(sys.argv[2])
	#Board GPIOs 4,17,27,22,5,6,13,19 used
        if pin_arg==0:
                pin = 4
        if pin_arg==1:
                pin = 17
        if pin_arg==2:
                pin = 27
        if pin_arg==3:
                pin = 22
        if pin_arg==4:
                pin = 5
        if pin_arg==5:
                pin = 6
        if pin_arg==6:
                pin = 13
        if pin_arg==7:
                pin = 19
	if DBG==1:
        	print 'Pin to Control is GPIO %s' % pin
        	print 'Value is %s' % val
        GPIO.setup(pin,GPIO.OUT)
        cur_val = GPIO.input(pin)
	if cur_val==0:
		ret_val=1;
	if cur_val==1:
		ret_val=0;
	print '%d' % ret_val
	if DBG==1:
        	print "Current value:%d" % cur_val
        if val >= 0:
		if val==0:
			set_val=1
		if val==1:
			set_val=0;
                GPIO.output(pin,set_val)
                new_val = GPIO.input(pin)
	if DBG==1:
                print "New value:%d" % new_val
        return ret_val

if __name__ == "__main__":
        sys.exit(main())

