import sys
from shutil import copyfile
from time import sleep
from StringIO import StringIO

import pyinotify
import requests
from PIL import Image, ImageEnhance

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

class Uploader(pyinotify.ProcessEvent):
    """
    Watch to_upload folder:
    when an image arrives
    - copy the image to another folder for printing
    - sends the image to the remove server
    """
    def __init__(self):
        super().__init__()
        self.url = "https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl"
        self.check_internet()
        self.path = None
        self.image = None
        print("Watching files to upload...")

    def process_IN_CREATE(self, event):
        """ Extract image path, run crop, save_for_printing and send to remote """
        self.path = event.pathname
        self.image = Image.open(self.path)
        print("A new image has arrived:", self.path)
        sleep(2)
        self.crop()
        self.save_for_printing()
        self.send_image()

    def crop(self):
        """ Crop image into a 1080px square"""
        box = (420, 0, 1500, 1080)
        self.image = self.image.crop(box)
        print("Image cropped")

    def save_for_printing(self):
        """ Save cropped image in to_print folder """
        self.image.save(self.path.replace("to_upload", "to_print"))
        print("Image copied to to_print")

    def send_image(self):
        """ send image to the remote server """
        # image = {'data': open(self.path, 'rb')
        # https://stackoverflow.com/questions/24247932/send-multiple-stringio-from-pil-image-in-post-requests-with-python
        # https://docs.python.org/2/library/stringio.html
        output = StringIO()
        self.image.save(output, "JPEG")
        output.seek(0)
        response = requests.post(self.url, files=output)
        try:
            response = response.raise_for_status()
            print("Image sucessfully sent")
        except requests.exceptions.RequestException as error:
            print("Error: {}".format(error))

    @classmethod
    def check_internet(cls):
        print("Checking internet connection...")
        test_url = "https://www.google.com"
        response = requests.get(test_url)
        print(response)
        try:
            response.raise_for_status()
            print("Internet is working")
        except:
            print("!!!Internet is down, check connection!!!")
            sys.exit()

HANDLER = Uploader()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./to_upload', MASK)

NOTIFIER.loop()
