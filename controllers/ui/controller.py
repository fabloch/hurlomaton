from tkinter import Tk, Frame
from .screen import Screen


class UIController(Tk):
    """
    Main GUI and page controller
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.is_fullscreen = True
        self.wm_attributes("-fullscreen", self.is_fullscreen)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for name in (
            "idle",
            "screaming",
            "fail",
            "success",
            "choice",
            "publishing",
            "bug",
        ):
            frame = Screen(
                parent=container,
                controller=self,
                width=self.screen["width"],
                height=self.screen["height"],
                name=name,
            )
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_idle()
        self.bind("<a>", self.show_idle)
        self.bind("<z>", self.show_screaming)
        self.bind("<e>", self.show_fail)
        self.bind("<r>", self.show_success)
        self.bind("<t>", self.show_choice)
        self.bind("<y>", self.show_publishing)
        self.bind("<u>", self.show_bug)

        self.bind("<f>", self.toggle_fullscreen)
        self.config(cursor="none")

    def show_idle(self, event=None):
        self.frames["idle"].show_up()

    def show_screaming(self, event=None):
        self.frames["screaming"].show_up()

    def show_fail(self, event=None):
        self.frames["fail"].show_up()

    def show_success(self, event=None):
        self.frames["success"].show_up()

    def show_choice(self, event=None):
        self.frames["choice"].show_up()

    def show_publishing(self, event=None):
        self.frames["publishing"].show_up()

    def show_bug(self, event=None):
        self.frames["bug"].show_up()

    def list_publish(self, event=None):
        """make the rotation list to show upload"""
        self.frames["publish"].fn_loop()

    def toggle_fullscreen(self, event=None):
        """ Toggles from fullscreen/windowed """
        self.is_fullscreen = not self.is_fullscreen
        self.wm_attributes("-fullscreen", self.is_fullscreen)

    @property
    def screen(self):
        """
        Returns a dictionnary with screen width and height
        """
        return {"width": self.winfo_screenwidth(), "height": self.winfo_screenheight()}
