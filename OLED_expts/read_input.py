import time
import Adafruit_SSD1306

import sys
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
		menu_option = 1
		GPIO.wait_for_edge(pin, GPIO.FALLING)
		time.sleep(0.25)
		menu_option = 0
		time.sleep(0.25)

def get_menu_selection(pin):
	global menu_select
	while True:
		menu_select = 1
		GPIO.wait_for_edge(pin, GPIO.FALLING)
		time.sleep(0.25)
		menu_select = 0
		time.sleep(0.25)

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
	get_ip_address_wrap()
	global TEXT
	global NET
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

def display():	
	global menu_option
	while True:
		if (menu_option == 1):
			display_clock()
		else:
			display_ip_addr()
			time.sleep(2)

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
RST = 16
pin = 7
menu_option = 1

color1_pin = 11
color2_pin = 13
color3_pin = 15

init_disp(RST)
config_input(pin)

x_offset = 10
y_offset = 10

try:
	thread.start_new_thread(display,())
	thread.start_new_thread(get_menu_option,(pin,))
	#thread.start_new_thread(control_tri_color_led,())
except:
	print 'Error starting threads!'

while 1:
	pass

