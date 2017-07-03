from picamera import PiCamera
from time import sleep
from gpiozero import Button

button = Button(17)
camera = PiCamera()

camera.start_preview()
button.wait_for_press()
camera.capture('/dev/huuulomaton/cam_test/captures/image3.jpg')
camera.stop_preview()
