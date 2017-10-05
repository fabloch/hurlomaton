import io
import requests
from time import sleep
from datetime import datetime
from picamera import PiCamera
from PIL import Image

class PhotoController(object):
    def __init__(self):
        self.camera = PiCamera()
        self.filepath = None

    def set_filepath(self, short_id):
        self.filepath = "./uploads/{0}.jpg".format(short_id)

    def run_all(self):
        image = self.take_photo()
        self.process_photo(image)

    def take_photo(self):
        stream = io.BytesIO()
        self.camera.capture(stream, format="jpeg")
        stream.seek(0)
        return Image.open(stream)

    def process_photo(self, image):
        box = (418, 58, 1502, 1142)
        region = image.crop(box)
        polaroid = Image.open("./media/polaroid.jpg")
        polaroid.paste(region, (50, 50))
        polaroid.save(self.filepath)

    def send_photo(self):
        url = 'https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl'
        file = {'data': open(self.filepath, "rb")}
        requests.post(url, files=file)

    def delete_photo(self):
        pass
