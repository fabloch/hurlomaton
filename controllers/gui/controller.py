"""
Graphical User Inferface module
"""
from time import sleep
from tkinter import Tk, Frame, font as tkfont
from itertools import cycle
from .slideshow import Slideshow
from .success import Success
from .upload import Upload
from .print import Print

class GUIController(Tk):
    """
    Main GUI and page controller
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.is_fullscreen = True
        self.wm_attributes('-fullscreen', self.is_fullscreen)
        self.fake_success = False

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page_class in (Slideshow, Success, Upload, Print):
            page_name = page_class.__name__
            frame = page_class(
                parent=container,
                controller=self,
                width=self.screen['width'],
                height=self.screen['height'],
            )
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_slideshow()
        self.bind("<b>", self.show_success)
        self.bind("<n>", self.show_slideshow)
        self.bind("<l>", self.show_print)
        self.bind("<f>", self.toggle_fullscreen)
        self.bind("<s>", self.mock_success)
        self.bind("<Escape>", self.end_gui)
        self.config(cursor="none")

    def show_success(self, event=None):
        '''Shows a frame for the given page name'''
        self.frames["Success"].show_up()

    def show_slideshow(self, event=None):
        '''Shows a frame for the given page name'''
        self.frames["Slideshow"].show_up()
        
    def show_print(self, event=None):
        '''Shows a frame for the given page name'''
        self.frames["Print"].show_up()
        
    def list_print(self, event=None):
        '''make the rotation list to show upload'''
        self.frames["Print"].loop()
    

    def toggle_fullscreen(self, event=None):
        """ Toggles from fullscreen/windowed """
        self.is_fullscreen = not self.is_fullscreen
        self.wm_attributes("-fullscreen", self.is_fullscreen)

    def end_gui(self, event=None):
        """ Closes the GUI """
        self.quit()

    def mock_success(self, event=None):
        self.fake_success = True
        self.after(1000, self.reset_success)

    def reset_success(self):
        self.fake_success = False

    @property
    def screen(self):
        """
        Returns a dictionnary with screen width and height
        """
        return {
            "width": self.winfo_screenwidth(),
            "height": self.winfo_screenheight()
        }
