from picamera import PiCamera
from time import sleep
import datetime

camera = PiCamera()


camera.start_preview()
sleep(8)
camera.capture('/home/pi/Desktop/cam_test/capture/image'+datetime.datetime.now()+'.jpg')
camera.stop_preview()
