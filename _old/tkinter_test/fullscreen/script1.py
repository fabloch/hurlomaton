import sys
from tkinter import *


class Fullscreen_Window:

    def __init__(self):
        self.root = Tk()
        self.root.wm_attributes('-fullscreen', 1)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.frame = Frame(self.root)
        self.frame.pack()
        self.state = False
        self.root.bind("<x>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.config(cursor="none")

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.wm_attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.wm_attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = Fullscreen_Window()
    w.root.mainloop()
