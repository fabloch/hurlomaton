from tkinter import Tk, Frame, Label, Button, font as tkfont

class SampleApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.is_fullscreen = True
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.wm_attributes('-fullscreen', self.is_fullscreen)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (Slideshow, Success):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame_slideshow()
        self.bind("<b>", self.show_frame_success)
        self.bind("<n>", self.show_frame_slideshow)
        self.bind("<f>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_gui)
        self.config(cursor="none")

    def show_frame_success(self, event=None):
        '''Show a frame for the given page name'''
        self.frames["Success"].tkraise()
        self.after(5000, self.frames["Slideshow"].tkraise)

    def show_frame_slideshow(self, event=None):
        '''Show a frame for the given page name'''
        self.frames["Slideshow"].tkraise()

    def toggle_fullscreen(self, event=None):
        """ Toggle from fullscreen/windowed """
        self.is_fullscreen = not self.is_fullscreen
        self.wm_attributes("-fullscreen", self.is_fullscreen)

    def end_gui(self, event=None):
        """ Close the GUI """
        self.destroy()

class Slideshow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

class Success(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Success", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
