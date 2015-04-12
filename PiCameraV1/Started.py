import time
import RPi.GPIO as GPIO
import datetime
import thread
import os

GPIO.setmode(GPIO.BCM)
shutdown_button = 21
click_button = 17
timer_button = 18
camera_mode_button = 19

#Shutdown button
GPIO.setup(shutdown_button, GPIO.IN, GPIO.PUD_UP)

#Output LEDs
# Green LED - Power indicator
pwr_indicator = 2
GPIO.setup(pwr_indicator, GPIO.OUT, GPIO.PUD_DOWN)

# Red LED - Click/Rec indicator
click_indicator = 3
GPIO.setup(click_indicator, GPIO.OUT, GPIO.PUD_DOWN)


#Turn on power indicator
GPIO.output(pwr_indicator, 1)

#Keep the default state of click indicator
GPIO.output(click_indicator, 0)

time.sleep(1)

def check_shutdown():
	while 1:
		GPIO.wait_for_edge(shutdown_button, GPIO.FALLING)
		print "Shutting down ...."
		GPIO.output (pwr_indicator, 0)
		os.system("sudo shutdown -h now")

def started_proc():
	while 1:
		GPIO.output(pwr_indicator,0)
		GPIO.output(click_indicator,1)
		time.sleep(0.5)
		GPIO.output(click_indicator,0)
		GPIO.output(pwr_indicator,1)
		time.sleep(0.5)

try:
	thread.start_new_thread(check_shutdown,())
	thread.start_new_thread(started_proc,())
except:
	print "Error starting procs!"

while 1:
	pass
