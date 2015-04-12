#Run this script as part of the rc.local
import time
import RPi.GPIO as GPIO
import picamera
import datetime

GPIO.setmode(GPIO.BCM)

#Camera click control
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)

#Camera click timer for selfies
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)

#Camera mode control - default(still/image), video recording
GPIO.setup(19, GPIO.IN, GPIO.PUD_UP)

while 1:
        delay = 0
        with picamera.PiCamera() as camera:
                camera.start_preview()
                if (GPIO.input(19) == 0):
                        GPIO.wait_for_edge(17, GPIO.FALLING)
                        camera.start_recording('/home/pi/test_video.h264')
                        time.sleep(1)
                        GPIO.wait_for_edge(17, GPIO.FALLING)
                        camera.stop_recording()
                else:
                        GPIO.wait_for_edge(17, GPIO.FALLING)
                        print "Taking snap... Say Cheese!"
                        today = datetime.date.today()
                        string = "PIC_" + str(today.day)+"_" + str(today.month)+"_" + str(today.year)+"_" + str(int(time.time())) + ".jpg"
                        path = "/var/www/img/"
                        filename = path + string
                        print filename
                        if(GPIO.input(18) == 0):
                                delay = 5
                        time.sleep(delay)
                        delay =0
                        camera.capture(filename)
                camera.stop_preview()

