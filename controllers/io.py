from RPi import GPIO


class IOController(object):
    def __init__(self):
        self.SOUND_INPUT_PORT = 2
        self.SPOTS_OUTPUT_PORT = 4
        self.YES_BUTTON_PORT = 18
        self.NO_BUTTON_PORT = 23

        self.sound_level_high = False
        self.yes_btn_pressed = False
        self.no_btn_pressed = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SOUND_INPUT_PORT, GPIO.IN)
        GPIO.setup(self.SPOTS_OUTPUT_PORT, GPIO.OUT)
        GPIO.setup(self.YES_BUTTON_PORT, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.NO_BUTTON_PORT, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.SOUND_INPUT_PORT, GPIO.BOTH, self.set_sound_switch)
        GPIO.add_event_detect(self.YES_BUTTON_PORT, GPIO.BOTH, self.set_yes_pressed)
        GPIO.add_event_detect(self.NO_BUTTON_PORT, GPIO.BOTH, self.set_no_pressed)

        GPIO.output(self.SPOTS_OUTPUT_PORT, False)

    def set_sound_switch(self, *args, **kwargs):
        self.sound_level_high = GPIO.input(self.SOUND_INPUT_PORT)

    def set_yes_pressed(self, *args, **kwargs):
        print("yes event detected:", GPIO.input(self.YES_BUTTON_PORT))
        self.yes_btn_pressed = not GPIO.input(self.YES_BUTTON_PORT)

    def set_no_pressed(self, *args, **kwargs):
        print("no event detected:", GPIO.input(self.YES_BUTTON_PORT))
        self.no_btn_pressed = not GPIO.input(self.NO_BUTTON_PORT)

    def spots_on(self, switch=False):
        GPIO.output(self.SPOTS_OUTPUT_PORT, switch)

    def cleanup(self):
        GPIO.cleanup()
