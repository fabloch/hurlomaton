from picamera import PiCamera
from time import sleep
from gpiozero import Button

from utils import now_string, path_to_images

button = Button(17)
camera = PiCamera()

camera.start_preview()

while True:
    try:
        button.wait_for_press()
        camera.capture("{path}/button/{now}.jpg".format(
            path=path_to_images(),
            now=now_string()))
    except KeyboardInterrupt:
        camera.stop_preview()
	break
