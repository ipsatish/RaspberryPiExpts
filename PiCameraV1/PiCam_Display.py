##############################################################################################
# This is a project to teach kids on how the day to day things work or built. The actual Camera
# is built with Lego blocks, with all the electronics is stuck inside.
# 
# Camera Project with RPi and PiCamera interfaced with 128x64 OLED display
# The PiCamera runs a webserver, which is used to display the images/videos
# Has a admin page, used to delete images/videos
# Wifi Mode:
#		- AP Mode - stand alone mode, no internet access. Outdoor use
#		- STA Mode - Connected to internet, used for sharing the videos on internet, updating 
#		  the system (Admin mode)
# 
# RPi GPIO interface:
# Board GPIOs (3,5) - I2C interface for the OLED display
# 			  16 - Reset for the Display (active-low)
# 			   7 - Menu Button
#			  23 - OK / Click Button
# Uses:
#	- hostapd (to run AP mode), need a custom hostapd for edimax dongle. Available on 
#     www.daveconroy.com website, also a copy available in this site.
#	- udhcpd - DHCP server
#	- apache (with PHP support) - Web server
#	- Uses Adafruit library for OLED display control
#	
# Author: Satish Panigatti (ipsatish@gmail.com)
# Date: 14 April 2015
##############################################################################################
 			  
import time
import Adafruit_SSD1306
import sys
import os
import socket
import fcntl
import struct
import picamera
import datetime
import thread
import Image
import ImageDraw
import ImageFont
import RPi.GPIO as GPIO

def config_input(pin):
	GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def init_disp(rst):
	global image
	global draw
	global width
	global height
	global disp
	global font
# 128x64 display with hardware I2C:
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(rst,GPIO.OUT)
	GPIO.output(rst,1)
	disp.begin()
# Clear display.
	disp.clear()
	disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))
# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
# Load default font.
	font = ImageFont.load_default()

def get_menu_option(pin):
	global menu_option
	while True:
		if (GPIO.input(pin) == 0):
			time.sleep(0.25)
			menu_option = menu_option + 1
			if (menu_option == 8):
				menu_option = 0
			time.sleep(0.25)

def get_menu_selection(pin):
	global menu_select
	while True:
		menu_select = 0
		if (GPIO.input(pin) == 0):
			time.sleep(0.25)
			menu_select = 1
			time.sleep(0.5)

# This function allows us to grab any of our IP addresses
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_ip_address_wrap():
	global TEXT
	global NET
# This sets TEXT equal to whatever your IP address is, or isn't
	try:
		NET = 'WLAN'
    		TEXT = get_ip_address('wlan0') # WiFi address of WiFi adapter. NOT ETHERNET
	except IOError:
    		try:
			NET = 'LAN'
        		TEXT = get_ip_address('eth0') # WiFi address of Ethernet cable. NOT ADAPTER
    		except IOError:
			NET = 'NONE'
        		TEXT = ('NO INTERNET!')


def display_ip_addr():
	global width
	global hieght
	global image
	global draw
	global disp
	global font
	global TEXT
	global NET
	if (NET == 'NONE'):
		get_ip_address_wrap()
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.rectangle((1, 1, 127, 63), outline=255, fill=0)
	message = 'Network Mode:' + NET
	draw.text((5+x_offset,5+y_offset),message,font=font, fill=255)
	message = 'You IP Address: '
	draw.text((5+x_offset,15+y_offset),message, font=font, fill=255)
	draw.text((5+x_offset,25+y_offset),TEXT,font=font,fill=255)
	disp.image(image)
	disp.display()

def display_clock():
	global width
	global hieght
	global image
	global draw
	global disp
	global font
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.rectangle((1, 1, 127, 63), outline=255, fill=0)
	text = time.strftime("%X")
	draw.text(((5+x_offset),(3+y_offset)),text,font=font, fill=255)
	text = time.strftime("%e %b %Y")
	draw.text(((5+x_offset),(15+y_offset)),text,font=font, fill=255)
	text = time.strftime("%A")
	draw.text(((5+x_offset),(25+y_offset)),text,font=font, fill=255)
	disp.image(image)
	disp.display()

def display_text(TEXT):
	global width, height, image, draw, disp, font
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.rectangle((1, 1, 127, 63), outline=255, fill=0)
	draw.text((5+x_offset,25+y_offset),TEXT,font=font,fill=255)
	disp.image(image)
	disp.display()

def camera_shutdown():
	global menu_select
	global shutdown
	if (shutdown == 0):
		display_text('Shutdown?')
	if (menu_select == 1 or shutdown == 1):
		display_text('Shutting down ...')
		time.sleep(1)
		shutdown = 1
		display_text('Good Bye! ...')
		time.sleep(1)
		os.system ('sudo shutdown now')

def camera_restart():
	global menu_select
	global restart  
	if (restart == 0):
		display_text('Restart?')
	if (menu_select == 1 or restart == 1):
		display_text('Restarting ...')
		restart = 1
		time.sleep(1)
		display_text('See you soon ...')
		time.sleep(1)
		os.system ('sudo reboot')

def still_camera_proc(delay):
	with picamera.PiCamera() as camera:
		if (menu_select == 1):
			display_text("Say Cheese!")
			today = datetime.date.today()
			string = "PIC_" + str(today.day)+"_" + str(today.month)+"_" + str(today.year)+"_" + str(int(time.time())) + ".jpg"
			path = "/var/www/img/"
			filename = path + string
			time.sleep(delay)
			camera.capture(filename)
			display_text("Done...")

def still_camera_dummy(delay):
	display_text("Still Camera Mode")

def video_camera_proc():
	with picamera.PiCamera() as camera:
		if (menu_select == 1):
			display_text("Recording...")
			#camera.start_recording('/var/www/img/test_video.h264.mp4')
			time.sleep(1)
		if (menu_select == 1):
			#camera.stop_recording()
			display_text("Recording Stop!")

def video_camera_dummy():
	display_text("Video Camera Mode")

# Have an option select between AP mode and STA mode
def wifi_mode():
	display_text("Wifi Mode")
	
def display():	
	global menu_option
	while True:
		if (menu_option == 0):
			display_clock()
		elif (menu_option == 1):
			still_camera_dummy(1)
		elif (menu_option == 2):
			still_camera_dummy(10)
		elif (menu_option == 3):
			video_camera_dummy()
		elif (menu_option == 4):
			wifi_mode()
		elif (menu_option == 5):
			display_ip_addr()
		elif (menu_option == 6):
			camera_shutdown()
		else:
			camera_restart()

# Raspberry Pi pin configuration(Board mode):
NET = 'NONE'
OLED_RST = 16
menu_option_pin = 7
menu_select_pin = 23

#Global variables for messaging between threads
menu_option = 0
menu_select = 0
shutdown = 0
restart = 0

#Default offset for printing text on the screen
x_offset = 10
y_offset = 10

init_disp(OLED_RST)
config_input(menu_option_pin)
config_input(menu_select_pin)

try:
	thread.start_new_thread(display,())
	thread.start_new_thread(get_menu_option,(menu_option_pin,))
	thread.start_new_thread(get_menu_selection,(menu_select_pin,))
except:
	print 'Error starting threads!'

while 1:
	pass

