import sys
from shutil import copyfile
from time import sleep
from io import StringIO

import pyinotify
import requests
from PIL import Image, ImageEnhance
from controllers import GPIOController
from RPi import GPIO
from datetime import datetime, timedelta

WM = pyinotify.WatchManager()

MASK = pyinotify.IN_CLOSE_WRITE# watched events

myGPIO = GPIOController()
succes_time_start=None
test_upload = False
test_print = False

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
        success_time_start = datetime.now()
        image = Image.open(self.path)
        self.crop(image, success_time_start)

    def crop(self, image, time):
        """ Crop image into a 1080px square"""
        box = (420, 0, 1500, 1080)
        #420,0,1500,1080
        result = image.crop(box)
        print("Image cropped")
        self.make_backgrounds(result, time)
        
    def make_backgrounds(self, image, time):
        size = (750, 750)
        position = (540,80)
        display_image = image.resize(size)
        
        background_1_print=Image.open("media/backup/fond-succes1-auray.jpg")
        background_1_print.paste(display_image,position)
        background_1_print.save("media/print/fond-print1.jpg")
        print("print 1 saved")
        
        
        background_2_print=Image.open("media/backup/fond-succes2-auray.jpg")
        background_2_print.paste(display_image,position)
        background_2_print.save("media/print/fond-print2.jpg")
        print("print 1 saved")
        
        print("background made")
        self.save_to_upload(image, time)

    def save_to_upload(self, image, time):
        """ saves cropped image in to_upload folder """
        
        image.save(self.path.replace("to_crop", "to_upload"))
        # self.raw_image.save(path)
        print("Image copied to to_upload")

        self.save_to_print(image, time)
        
    def save_to_print(self,image, time):
        """Asks user if he wants a printed copy of the photo
        then fuse cropped image with background image and save it in print folder if yes"""
        
        success_time_delta = datetime.now() - time
        print("Do you want to print ?")
        while (GPIO.input(myGPIO.YES_BUTTON_PORT) == 1 and GPIO.input(myGPIO.NO_BUTTON_PORT) == 1 
        or GPIO.input(myGPIO.YES_BUTTON_PORT) == 0 and GPIO.input(myGPIO.NO_BUTTON_PORT) == 0
        or success_time_delta >= timedelta(seconds=10) and success_time_delta <= timedelta(seconds=20)):
            
            success_time_delta = datetime.now() - time
        
            if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
                sleep(1)
                background=Image.open("media/polaroid01.jpg")
                #takes a background for the polaroid
                background.paste(image,(50,40))
                #paste the photo on the background
                background.save(self.path.replace("to_crop", "to_print"))
                print("Image copied to to_print")
                break
            
            elif (GPIO.input(myGPIO.NO_BUTTON_PORT) == 0
                  or success_time_delta >= timedelta(seconds=20)):
                sleep(1)
                print("image NOT copied to to_print")
                break
        
        print("done")

HANDLER = Cropper()
NOTIFIER = pyinotify.Notifier(WM, HANDLER)

WDD = WM.add_watch('./to_crop', MASK)

NOTIFIER.loop()
