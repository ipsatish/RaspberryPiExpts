import time
import Adafruit_SSD1306

import sys
import os
import socket
import fcntl
import struct

import thread

import Image
import ImageDraw
import ImageFont
import RPi.GPIO as GPIO
import sys, getopt

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
	GPIO.output(rst,0)
	time.sleep(0.5)
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
		#menu_option = 1
		#GPIO.wait_for_edge(pin, GPIO.FALLING)
		if (GPIO.input(pin) == 0):
			time.sleep(0.25)
			menu_option = menu_option + 1
			print 'DEBUG: menu_option=%d' % menu_option
			if (menu_option == 5):
				menu_option = 0
			time.sleep(0.25)

def get_menu_selection(pin):
	global menu_select
	while True:
		menu_select = 0
		#GPIO.wait_for_edge(pin, GPIO.FALLING)
		if (GPIO.input(pin) == 0):
			time.sleep(0.25)
			menu_select = 1
			print 'DEBUG: menu_select=%d' % menu_select
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

def display_image():
	global width, height, image, draw, disp, font
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	image1 = Image.open('happycat_oled_64.ppm').convert('1')
	disp.image(image1)
	disp.display()

def display_text(TEXT):
	global width, height, image, draw, disp, font
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.rectangle((1, 1, 127, 63), outline=255, fill=0)
	draw.text((5+x_offset,25+y_offset),TEXT,font=font,fill=255)
	disp.image(image)
	disp.display()

def option_shutdown():
	global menu_select
	global shutdown
	if (shutdown == 0):
		display_text('Shutdown?')
	if (menu_select == 1 or shutdown == 1):
		display_text('Shutting down ...')
		shutdown = 1
		print 'DEBUG: shutdown %d' % shutdown
		time.sleep(1)
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		os.system ('sudo shutdown now')

def option_restart():
	global menu_select
	global restart  
	if (restart == 0):
		display_text('Restart?')
	if (menu_select == 1 or restart == 1):
		display_text('Restarting ...')
		print 'DEBUG: restart %d' % restart
		restart = 1
		time.sleep(1)
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		os.system ('sudo reboot')

def display1():	
	global menu_option
	while True:
		if (menu_option == 0):
			display_clock()
		else:
			display_ip_addr()
			time.sleep(2)

def display2():	
	global menu_option
	while True:
		if (menu_option == 0):
			display_clock()
			print 'DEBUG: main loop %d' % menu_option
		elif (menu_option == 1):
			display_ip_addr()
			print 'DEBUG: main loop %d' % menu_option
			time.sleep(2)
			menu_option = 2
		elif (menu_option == 2):
			display_image()	
			print 'DEBUG: main loop %d' % menu_option
		elif(menu_option == 3):
			option_shutdown()
			print 'DEBUG: main loop %d' % menu_option
		else:
			option_restart()
			print 'DEBUG: main loop %d' % menu_option

def display():	
	global menu_option
	while True:
		if (menu_option == 0):
			display_clock()
			print 'DEBUG: main loop %d' % menu_option
		elif (menu_option == 1):
			option_restart()
			print 'DEBUG: main loop %d' % menu_option
		elif(menu_option == 2):
			option_shutdown()
			print 'DEBUG: main loop %d' % menu_option
		else:
			display_ip_addr()
			time.sleep(2)
			menu_option = 0
			print 'DEBUG: main loop %d' % menu_option

def tri_color_led(color1, color2, color3):
	global color1_pin, color2_pin, color3_pin
	GPIO.setup(color1_pin, GPIO.OUT)
	GPIO.setup(color2_pin, GPIO.OUT)
	GPIO.setup(color3_pin, GPIO.OUT)
	GPIO.output(color1_pin,color1)
	GPIO.output(color2_pin,color2)
	GPIO.output(color3_pin,color3)

def control_tri_color_led():
	while True:
		tri_color_led(1,1,1)
		time.sleep(0.5)
		tri_color_led(1,1,0)
		time.sleep(0.5)
		tri_color_led(1,0,1)
		time.sleep(0.5)
		tri_color_led(0,1,1)
		time.sleep(0.5)
		tri_color_led(1,0,0)
		time.sleep(0.5)
	
	
# Raspberry Pi pin configuration:
NET = 'NONE'
RST = 16
menu_option_pin = 7
menu_select_pin = 23
menu_option = 0
menu_select = 0
shutdown = 0
restart = 0

color1_pin = 11
color2_pin = 13
color3_pin = 15

init_disp(RST)
config_input(menu_option_pin)
config_input(menu_select_pin)

x_offset = 10
y_offset = 10

try:
	thread.start_new_thread(display,())
	thread.start_new_thread(get_menu_option,(menu_option_pin,))
	thread.start_new_thread(get_menu_selection,(menu_select_pin,))
	#thread.start_new_thread(control_tri_color_led,())
except:
	print 'Error starting threads!'

while 1:
	pass

