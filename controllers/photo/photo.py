import io
import requests
from time import sleep
from datetime import datetime
from picamera import PiCamera
from PIL import Image

class PhotoController(object):
    def __init__(self):
        self.camera = PiCamera()
        self.short_id = None
        self.image = None

    def set_short_id(self, short_id):
        self.short_id = short_id

    def take_photo(self):
        stream = io.BytesIO()
        self.camera.capture(stream, format="jpeg")
        stream.seek(0)
        self.image = Image.open(stream)

    def process_photo(self, image):
        box = (418,58, 1502, 1142)
        region = image.crop(box)
        polaroid = Image.open("./media/polaroid.jpg")
        polaroid.paste(region, (50, 50))
        polaroid.name = self.short_id + ".jpg"
        return polaroid

    @classmethod
    def send_photo(cls, image):
        url = 'https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl'
        file = {'data': image}
        requests.post(url, files=file)


    def delete_photo(self):
        pass
