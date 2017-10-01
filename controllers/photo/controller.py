from time import sleep
from datetime import datetime
from picamera import PiCamera

class PhotoController(object):
    def __init__(self):
        self.camera = PiCamera()
        self.short_id = None

    def set_short_id(self, short_id):
        self.short_id = short_id

    def take_photo(self):
        if self.short_id:
            self.camera.capture("./uploads/{0}.jpg".format(self.short_id))
        else:
            print("Error with short_id")

    def send_photo(self):
        pass

    def delete_photo(self):
        pass
