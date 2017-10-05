import pyinotify
from time import sleep
import sys

import requests

import subprocess

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

class Uploader(pyinotify.ProcessEvent):
    def __init__(self):
        super().__init__()
        self.url = "https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl"
        self.check_internet()
        print("Watching incoming files in uploads...")

    def process_IN_CREATE(self, event):
        path = event.pathname
        print("Uploading in two seconds:", path)
        sleep(2)
        self.print_image(event.path)
        self.send_image(event.path)

    @classmethod
    def print_image(cls, path):
        print("Printing image...")
        command = "lp -d selphy_cp1200 {0}".format(path)
        print(command)
        subprocess.call(command)
        
    @classmethod
    def send_image(clas, path):
        image = {'data': open(path, 'rb')}
        response = requests.post(self.url, files=image)
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
            print("Connected :)")
        except:
            print("!!!Internet is down, check connection!!!")
            sys.exit()
 

HANDLER = Uploader()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./uploads', MASK)

NOTIFIER.loop()
