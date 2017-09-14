from picamera import PiCamera
from time import sleep
from gpiozero import Button

from utils import now_string, path_to_images

button = Button(17)
camera = PiCamera()

# 44amera.start_preview()

while True:
    try:
        while True:
            if button.is_pressed:
                pass
            else:
                camera.capture("{path}/button/{now}.jpg".format(
                    path=path_to_images(),
                    now=now_string()))
                sleep(10)
                break
        # break
    except KeyboardInterrupt:
        camera.stop_preview()
        break

