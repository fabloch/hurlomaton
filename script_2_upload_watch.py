import sys
from shutil import copyfile
from time import sleep
from io import StringIO

import pyinotify
import requests
from PIL import Image, ImageEnhance

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

class Uploader(pyinotify.ProcessEvent):
    """
    Watch to_upload folder:
    when an image arrives
    - sends the image to the remove server
    - process image for printing and sends in to_print 
    """
    def __init__(self):
        super().__init__()
        self.url = "https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl"
        # self.check_internet()
        self.path = None
        self.image = None
        print("Watching files to upload...")

    def process_IN_CREATE(self, event):
        """ Extract image path, run crop, save and send to remote """
        self.path = event.pathname
        print("A new image has arrived:", self.path)
        sleep(2)
        self.image = Image.open(self.path)
        self.process_for_printing()
        self.save_to_print()
        self.send_image()

    def process_for_printing(self):
        """ Paste square photo into polaroid """
        photo = Image.open(self.path)
        self.image = Image.open("./media/polaroid.jpg")
        self.image.paste(photo, (51, 51))
        
    def save_to_print(self):
        """ Save cropped image in both folders """
        self.image.save(self.path.replace("to_upload", "to_print"))
        # self.raw_image.save(self.path)
        print("Image copied to to_print")

    def send_image(self):
        """ send image to the remote server """
        # image = {'data': open(self.path, 'rb')
        # https://stackoverflow.com/questions/24247932/send-multiple-stringio-from-pil-image-in-post-requests-with-python
        # https://docs.python.org/2/library/stringio.html
        file = {'data': open(self.path, 'rb')}
        response = requests.post(self.url, files=file)
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
