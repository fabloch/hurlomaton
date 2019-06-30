import os
import glob

from picamera import PiCamera
from PIL import Image

from utils import CONST


class CaptureController(object):
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.path = "ramdisk/capture.jpg"

    def take_photo(self):
        self.camera.capture(self.path)

    def process(self):
        full_img = Image.open(self.path)
        box = (420, 0, 1500, 1080)
        cropped_img = full_img.crop(box)

        """ creating image for choice screen """
        size = (720, 720)
        screen_img = cropped_img.resize(size)
        position = (266, 326)
        background_img = Image.open("media/{}/choice.jpg".format(CONST["EVENT_NAME"]))
        background_img.paste(screen_img, position)
        background_img.save("ramdisk/choice_screen.jpg")

        """ creating polaroid """
        polaroid = Image.open("media/{}/polaroid.jpg".format(CONST["EVENT_NAME"]))
        polaroid.paste(cropped_img, (50, 40))
        polaroid.save("ramdisk/polaroid.jpg")

    def clean_ramdisk(self):
        files = glob.glob("ramdisk/*")
        for f in files:
            os.remove(f)
        print("ramdisk files cleaned.")
