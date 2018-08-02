import sys
from shutil import copyfile
from time import sleep
from io import StringIO

import pyinotify
import requests
from PIL import Image, ImageEnhance

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CLOSE_WRITE  # watched events

POLA = Image.open("media/polaroid01.jpg", mode="r") #load base polaroid

class Cropper(pyinotify.ProcessEvent):
    """
    Watch to_crop folder:
    when an image arrives
    - crops the image
    - sends the cropped image to to_upload
    """
    def __init__(self):
        super().__init__()
        self.url = "https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl"
        self.path = None
        print("Watching files to crop...")

    def process_IN_CLOSE_WRITE(self, event):
        """ Extract image path, run crop, save in to_upload"""
        self.path = event.pathname
        print("A new image has arrived:", self.path)
        image = Image.open(self.path)
        self.crop(image)

    def crop(self, image):
        """ Crop image into a 1080px square"""
        box = (420, 0, 1500, 1080)
        result = image.crop(box)
        print("Image cropped")
        # self.save_to_upload(result)
        self.create_pola(result)

    def create_pola(self, image):
        POLA.paste(image, box=(50,50)) #put croped image on top of base polaroid
        print("Polaroid made")
        POLA.save(self.path.replace("to_crop", "to_print")) # save result
        print("Image copied to to_print")
#        self.save_to_print(result)

#    def save_to_print(self, image):
#        """ Save cropped image in both folders """
#        image.save(self.path.replace("to_crop", "to_print"))
#        print("Image copied to to_print")

    # def save_to_upload(self, image):
    #     """ Save cropped image in both folders """
    #     image.save(self.path.replace("to_crop", "to_upload"))
    #     # self.raw_image.save(path)
    #     print("Image copied to to_upload")

HANDLER = Cropper()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./to_crop', MASK)

NOTIFIER.loop()
