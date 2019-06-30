import glob
from itertools import cycle
from tkinter import Frame, Label
from PIL import Image, ImageTk, ImageOps
from utils import CONST


class Screen(Frame):
    def __init__(self, parent, controller, width, height, name):
        Frame.__init__(self, parent)
        self.controller = controller
        self.size = (width, height)
        self.name = name
        self.slideshow = Label(self, background="black")
        self.slideshow.pack(side="top", fill="x")

        self.delay = CONST["IDLE_DELAY_MS"]
        self.image_loop = cycle(self.image_list())

        self.play()

    def image_list(self):
        """
        Loads images files from
        /media/<event_name>/
        using the "name" param to filter images
        """
        images = []
        selection = [
            f
            for f in glob.glob(
                "./media/{folder}/*.*".format(folder=CONST["MEDIA_FOLDER"])
            )
            if self.name in f
        ]

        for f in selection:
            image = Image.open(f)
            resized_img = ImageOps.fit(image, self.size, Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_img)
            images.append(tk_image)
        return images

    def play(self):
        """
        Cycles through the images from image list
        """
        img_object = next(self.image_loop)
        self.slideshow.config(image=img_object)
        self.after(self.delay, self.play)

    def show_up(self):
        """
        Brings to front
        !!! Hack for choice screen refresh !!!
        """
        if self.name is "choice":
            image = Image.open("ramdisk/choice_screen.jpg")
            resized_img = ImageOps.fit(image, self.size, Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_img)
            self.image_loop = cycle([tk_image])

        self.tkraise()
