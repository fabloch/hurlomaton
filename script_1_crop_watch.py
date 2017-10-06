import sys
from shutil import copyfile
from time import sleep
from io import StringIO

import pyinotify
import requests
from PIL import Image, ImageEnhance

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

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
        print("Watching files to crop...")

    def process_IN_CREATE(self, event):
        """ Extract image path, run crop, save in to_upload"""
        path = event.pathname
        print("A new image has arrived:", path)
        image = Image.open(path)
        self.crop(image)

    def crop(self, image):
        """ Crop image into a 1080px square"""
        box = (420, 0, 1500, 1080)
        image = image.crop(box)
        print("Image cropped")
        self.save_to_upload(image)

    def save_to_upload(self, image):
        """ Save cropped image in both folders """
        image.save(path.replace("to_crop", "to_upload"))
        # self.raw_image.save(path)
        print("Image copied to to_upload")

HANDLER = Cropper()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./to_crop', MASK)

NOTIFIER.loop()
