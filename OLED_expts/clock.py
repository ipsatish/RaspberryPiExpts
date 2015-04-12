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

def get_input(pin):
	global count
	while True:
		GPIO.wait_for_edge(pin, GPIO.FALLING)
		print 'Button pressed'
		count = count+1

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
	message = 'Network Mode: ' + NET
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
	while True:
		display_clock()
		time.sleep(2)
		display_ip_addr()
		time.sleep(2)

#try:
#	thread.start_new_thread(display,)
#	thread.start_new_thread(get_input,)
#except:
#	print 'Error starting threads!'

# Raspberry Pi pin configuration:
RST = 16
pin = 7

# Initialize library.
init_disp(RST)

config_input(pin)

x_offset = 10
y_offset = 10

display()
