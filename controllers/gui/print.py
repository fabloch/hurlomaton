"""
Slideshow page module
"""
import glob
from itertools import cycle
from tkinter import Frame, Label
from PIL import Image, ImageTk, ImageOps


class Print(Frame):
    """
    Slideshow page class
    """
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.controller = controller
        self.size = (width, height)
        self.print = Label(self, background="grey")
        self.print.pack(side="top", fill="x")
        

        self.delay = 500
        self.image_loop = None
        
    def fn_loop(self):
        image_number = 0
        images = []
        for img_file in glob.glob('./media/print/*.*'):
            image = Image.open(img_file)
            resized_img = ImageOps.fit(image, self.size, Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_img)
            images.append(tk_image)
            image_number += 1
            print("loaded image #", image_number)
        self.image_loop = cycle(images)
        var_loop = self.image_loop
        self.play(var_loop)

    #def image_list(self):
        """
        Loads images files from the image_folder directory
        into a list of tk compatible images
        """
    #    image_number = 0
    #    images = []
    #    for img_file in glob.glob('./media/print/*.*'):
    #        image = Image.open(img_file)
    #        resized_img = ImageOps.fit(image, self.size, Image.ANTIALIAS)
    #        tk_image = ImageTk.PhotoImage(resized_img)
    #        images.append(tk_image)
    #        image_number += 1
    #        print("loaded image #" + str(image_number))
    #    return images

    def play(self, images):
        """
        Cycles through the images from image list
        """
        img_object = next(images)
        self.print.config(image=img_object)
        self.after(self.delay, self.play)
        
     

    def show_up(self):
        """
        Brings to front
        """
        self.tkraise()