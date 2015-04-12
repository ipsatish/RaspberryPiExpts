import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
shutdown_button = 21
click_button = 17
timer_button = 18
camera_mode_button = 19

#Camera click timer for selfies
GPIO.setup(timer_button, GPIO.IN, GPIO.PUD_UP)

#Camera mode control - default(still/image), video recording
GPIO.setup(camera_mode_button, GPIO.IN, GPIO.PUD_UP)

while 1:
	print "Camera button mode: %d " % GPIO.input(camera_mode_button)
	time.sleep(1)
