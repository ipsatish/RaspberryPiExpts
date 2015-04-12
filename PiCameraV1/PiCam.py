import time
import RPi.GPIO as GPIO
import picamera
import datetime
import thread
import os

GPIO.setmode(GPIO.BCM)
shutdown_button = 21
click_button = 17
timer_button = 18
camera_mode_button = 19

#Camera click control
GPIO.setup(click_button, GPIO.IN, GPIO.PUD_UP)

#Camera click timer for selfies
GPIO.setup(timer_button, GPIO.IN, GPIO.PUD_UP)

#Camera mode control - default(still/image), video recording
# 0 - Video Rec
# 1 - Still Camera Mode
GPIO.setup(camera_mode_button, GPIO.IN, GPIO.PUD_UP)

#Shutdown button
GPIO.setup(shutdown_button, GPIO.IN, GPIO.PUD_UP)

#Output LEDs
# Green LED - Power indicator
pwr_indicator = 2
GPIO.setup(pwr_indicator, GPIO.OUT, GPIO.PUD_DOWN)

# Red LED - Click/Rec indicator
click_indicator = 3
GPIO.setup(click_indicator, GPIO.OUT, GPIO.PUD_DOWN)

#Variable Share Status
click_pressed = 0
camera_mode = 0

#Turn on power indicator
GPIO.output(pwr_indicator, 1)

#Keep the default state of click indicator
GPIO.output(click_indicator, 0)

def check_shutdown():
	while 1:
		GPIO.wait_for_edge(shutdown_button, GPIO.FALLING)
		print "Shutting down ...."
		GPIO.output (pwr_indicator, 0)
		os.system("sudo shutdown -h now")

def video_rec_indicator():
	global click_pressed
	print "In Video rec indicator"
	while (click_pressed == 1) :  
		GPIO.output(click_indicator,1)
		time.sleep(0.25)
		GPIO.output(click_indicator,0)
		time.sleep(0.25)
	GPIO.output(click_indicator, 0)

def check_camera_mode():
	global camera_mode
	while 1:
		camera_mode = GPIO.input(camera_mode_button)
		time.sleep (0.1)
		
def camera_proc():
	global click_pressed
	global camera_mode
	while 1:
		delay = 0
		with picamera.PiCamera() as camera:
			camera.start_preview()
			if (camera_mode == 0):
				print "Camera Mode: Video"
				GPIO.wait_for_edge(click_button, GPIO.FALLING)
				click_pressed = 1
				try:
					thread.start_new_thread(video_rec_indicator,())
				except:
					print "Error starting proc: video_rec_indicator!"
				print "Recording started .."
				#camera.start_recording('/var/www/img/test_video.h264.mp4')
				time.sleep(1)
				GPIO.wait_for_edge(click_button, GPIO.FALLING)
				#camera.stop_recording()
				click_pressed = 0
				print "Recording stopped .."
			else:
				print "Camera Mode: Still"
				GPIO.wait_for_edge(click_button, GPIO.FALLING)
				GPIO.output(click_indicator, 1)
				print "Taking snap... Say Cheese!"
				today = datetime.date.today()
				string = "PIC_" + str(today.day)+"_" + str(today.month)+"_" + str(today.year)+"_" + str(int(time.time())) + ".jpg"
				path = "/var/www/img/"
				filename = path + string
				print filename
				if(GPIO.input(timer_button) == 0):
					delay = 9
				time.sleep(delay)
				delay =0
				camera.capture(filename)
				GPIO.output(click_indicator, 0)
			camera.stop_preview()

def new_camera_proc():
	global click_pressed
	global camera_mode
	while 1:
		delay = 0
		with picamera.PiCamera() as camera:
			GPIO.wait_for_edge(click_button, GPIO.FALLING)
			camera.start_preview()
			if (camera_mode == 0):
				print "Camera Mode: Video"
				click_pressed = 1
				try:
					thread.start_new_thread(video_rec_indicator,())
				except:
					print "Error starting proc: video_rec_indicator!"
				print "Recording started .."
				#camera.start_recording('/var/www/img/test_video.h264.mp4')
				time.sleep(1)
				GPIO.wait_for_edge(click_button, GPIO.FALLING)
				#camera.stop_recording()
				click_pressed = 0
				print "Recording stopped .."
			else:
				print "Camera Mode: Still"
				GPIO.wait_for_edge(click_button, GPIO.FALLING)
				GPIO.output(click_indicator, 1)
				print "Taking snap... Say Cheese!"
				today = datetime.date.today()
				string = "PIC_" + str(today.day)+"_" + str(today.month)+"_" + str(today.year)+"_" + str(int(time.time())) + ".jpg"
				path = "/var/www/img/"
				filename = path + string
				print filename
				if(GPIO.input(timer_button) == 0):
					delay = 9
				time.sleep(delay)
				delay =0
				camera.capture(filename)
				GPIO.output(click_indicator, 0)
			camera.stop_preview()
try:
	thread.start_new_thread(check_shutdown,())
	thread.start_new_thread(new_camera_proc,())
	thread.start_new_thread(check_camera_mode,())
except:
	print "Error starting procs!"

while 1:
	pass
