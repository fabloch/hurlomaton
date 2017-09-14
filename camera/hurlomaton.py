import RPi.GPIO as GPIO
import time

from picamera import PiCamera
from time import sleep
from datetime import datetime
from utils import now_string, path_to_images

camera = PiCamera()
bridgefile = "/home/pi/Desktop/huuurlomaton/bridge/share-python-data.txt"
photofolder = "/home/pi/Desktop/huuurlomaton/interface/public/client/static/img/photos/"
noisedetected = False

def oldprocess():
	camera.start_preview()
	sleep(3)
	camera.capture("{path}/capture/{now}.jpg".format(
		path=path_to_images(),
		now=now_string()))
	camera.stop_preview()

""" ________WRITE IN FILE_________ """

def writeinfile(stepstr, filename):
	f = open(filename,"w")
	f.write(stepstr)
	f.close() 

""" ________TAKE PICTURE_________ """

def takepicture():
	imagename = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
	print( deleteblank(deletetwodot(imagename)) )
	imageid = 9999
	camera.start_preview()
	camera.capture(photofolder+imagename+".jpg".format(
		path=path_to_images(),
		now=now_string()))
	camera.stop_preview()
	return imagename
	
""" ________EPURE STRING_________ """
def deletetwodot(str):
	return str.replace(":","")
	
def deleteblank(str):
	return str.replace(" ","").replace("\t","").replace("\n","")

""" ________COMPOSE STRING FOR FILE_________ """

def strstep4():
	stepstr = """
				{
				"step":4,
				"image":"old.jpg",
				"number":"98989898"
				}
			"""
	return deleteblank(stepstr)
	
def strstep3(image, imgnumber):
	stepstr = """
				{
				"step":3,
				"image":"/static/img/photos/%s.jpg",
				"number":"%s"
				}
			"""% (image, imgnumber)
	return deleteblank(stepstr)
	
def strstep2():
	stepstr = """
				{
				"step":2,
				"image":"old.jpg",
				"number":"98989898"
				}
			"""
	return deleteblank(stepstr)
	
def strstep1():
	stepstr = """
				{
				"step":1,
				"image":"old.jpg",
				"number":"98989898"
				}
			"""
	return deleteblank(stepstr)
	
""" ___________LAUCH STEP_____________ """

def writestep4():
	print("in step 4")
	newstr = strstep4()
	writeinfile(newstr, bridgefile)
	
def writestep3(image, number):
	print("in step 3")
	newstrstep3 = strstep3(image, number)
	writeinfile(newstrstep3, bridgefile)

def writestep2():
	print("in step 2")
	newstr = strstep2()
	writeinfile(newstr, bridgefile)

def writestep1():
	print("in step 1")
	newstr = strstep1()
	writeinfile(newstr, bridgefile)

""" ___________CALLBACK LAUCHED WHEN GPIO-16 TRIGGERED_____________ """
def triggerphoto(self):
	global noisedetected
	print(noisedetected)
	if (GPIO.input(16)):
		noisedetected = True
		print("pushedpeshed")
	else:
		noisedetected = False
		print("..........")		


def startprocess():
	while True:
		print("hello world")
		writestep1()
		if(noisedetected == True):
			sleep(2)
			if(noisedetected == True):
				newimage = takepicture()
				writestep2()
				sleep(2)
				writestep3(newimage, "temp")
				sleep(15)
			else:
				writestep4()
				sleep(5)
				
		else:
			sleep(2)
			
	
writeinfile("nique tout", bridgefile)

GPIO.setmode(GPIO.BCM)

GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(16, GPIO.BOTH)

GPIO.add_event_callback(16, triggerphoto)

startprocess()

print("terminate")
