import pyinotify
import requests
import os

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

class Uploader(pyinotify.ProcessEvent):
    def __init__(self):
        super().__init__()
        self.url = "https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl"

    def process_IN_CREATE(self, event):
        print("Uploading:", event.pathname)
        image = {'data': open(event.pathname, 'rb')}
        response = requests.post(self.url, files=image)
        try:
            response.raise_for_status()
            print(response)
        except requests.exceptions.RequestException as error:
            print("Error: {}".format(error))

HANDLER = Uploader()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./uploads', MASK)

NOTIFIER.loop()
