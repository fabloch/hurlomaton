import RPi.GPIO as GPIO
import time

"""
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)
print "led on"
GPIO.output(16,GPIO.HIGH)
time.sleep(3)
print "led off"
GPIO.output(16,GPIO.LOW)
"""

GPIO.setmode(GPIO.BCM)

GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(16, GPIO.RISING)
def my_callback():
	print "pushedpeshed"
GPIO.add_event_callback(16, my_callback)
