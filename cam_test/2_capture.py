from picamera import PiCamera
from time import sleep

from utils import now_string, path_to_images

camera = PiCamera()

camera.start_preview()
sleep(4)
camera.capture("{path}/capture/{now}.jpg".format(
    path=path_to_images(),
    now=now_string()))
camera.stop_preview()
