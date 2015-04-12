import Adafruit_SSD1306
import time
import sys
import socket
import fcntl
import struct
import thread
import os

import Image
import ImageDraw
import ImageFont
import RPi.GPIO as GPIO

def config_input(pin):
	GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def init_disp(rst):
	global width, height, image, draw, disp, font
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
		GPIO.wait_for_edge(pin, GPIO.FALLING)
		time.sleep(0.25)
		menu_option = menu_option + 1
		if (menu_option == 5):
			menu_option = 0
		time.sleep(0.25)

def get_menu_selection(pin):
	global menu_select
	while True:
		menu_select = 0
		time.sleep(0.1)
		GPIO.wait_for_edge(pin, GPIO.FALLING)
		time.sleep(0.25)
		menu_select = 1
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
	global TEXT, NET
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
	global width, height, image, draw, disp, font, TEXT, NET
	get_ip_address_wrap()
	disp.clear()
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
	global width, height, image, draw, disp, font
	disp.clear()
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
		restart = 1
		time.sleep(1)
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		os.system ('sudo reboot')


def display():	
	global menu_option
	while True:
		if (menu_option == 0):
			display_clock()
		else:
			if (menu_option == 1):
				display_ip_addr()
			else:
				if (menu_option == 2):
					display_image()	
				else:
					if(menu_option == 3):
						option_shutdown()
					else:
						option_restart()

	
# Raspberry Pi pin configuration:
RST = 16
menu_option_pin = 7
menu_select_pin = 11
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
except:
	print 'Error starting threads!'

while 1:
	pass

