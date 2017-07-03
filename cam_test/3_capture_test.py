from picamera import PiCamera
from time import sleep
from datetime import datetime
format = '%Y-%m-%d %H:%M:%S'

now = datetime.now()
newtime = now.strftime("%Y-%m-%d-%H-%M-%S")
       
camera = PiCamera()


camera.start_preview()
sleep(8)
camera.capture('/home/pi/Desktop/cam_test/capture/hurlomaton'+newtime+'.jpg')
camera.stop_preview()
