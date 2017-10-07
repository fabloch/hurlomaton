import subprocess
from time import sleep

import pyinotify
from PIL import Image

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CREATE  # watched events

class Printer(pyinotify.ProcessEvent):
    """
    Watch to_print folder:
    when an image arrives
    - process the image into a polaroid
    - prints the image
    """
    def __init__(self):
        super().__init__()
        self.path = ""
        print("Watching files to print...")

    def process_IN_CREATE(self, event):
        """ Extract the image path, process and print """
        self.path = event.pathname
        print("A new image has arrived:", self.path)
        sleep(2)
        self.print()

    def print(self):
        """ Send print command to """
        print("Printing image...")
        # command = "sudo /usr/bin/lp -d selphy_cp1200 uploads/UEZOFEQCC.jpg, shell=True"
        command = "sudo /usr/bin/lp -d selphy_cp1200 {0}".format(self.path)
        # print(command)
        sub = subprocess.call(command, shell=True)

HANDLER = Printer()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./to_print', MASK)

NOTIFIER.loop()
