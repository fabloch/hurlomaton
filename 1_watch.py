import pyinotify
import requests
import os
import sys
from time import sleep

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

class Uploader(pyinotify.ProcessEvent):
    def __init__(self):
        super().__init__()
        self.url = "https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl"
        self.check_internet()
        print("Watching incoming files in uploads...")

    def process_IN_CREATE(self, event):
        print("Uploading in two seconds:", event.pathname)
        sleep(2)

    def check_internet(self):
        print("Checking internet connection...")
        test_url = "https://www.google.com"
        response = requests.get(test_url)
        print(response)
        try:
            response.raise_for_status()
            print("Connected :)")
        except:
            print("Internet is down, check connection :(")
            sys.exit()
    def print_image(self, event):
        
    def send_image(self, event):
        image = {'data': open(event.pathname, 'rb')}
        response = requests.post(self.url, files=image)
        try:
            response = response.raise_for_status()
            print("Image sucessfully sent")
        except requests.exceptions.RequestException as error:
            print("Error: {}".format(error))

HANDLER = Uploader()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./uploads', MASK)

NOTIFIER.loop()
