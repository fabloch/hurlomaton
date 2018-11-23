import io
import requests
from time import sleep
from datetime import datetime
from picamera import PiCamera
from PIL import Image

class PhotoController(object):
    def __init__(self):
        self.camera = PiCamera()
        self.pathname = None

    def set_filepath(self, short_id):
        self.pathname = "./to_crop/{0}.jpg".format(short_id)

    def capture(self):
        self.camera.capture(self.pathname)
