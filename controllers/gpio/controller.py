from time import sleep, time
from RPi import GPIO

class GPIOController(object):
    def __init__(self):
        self.SOUND_INPUT_PORT = 2
        self.SPOTS_OUTPUT_PORT = 4
        self.sound_level_high = False
        self.YES_BUTTON_PORT = 18
        self.NO_BUTTON_PORT = 23
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SOUND_INPUT_PORT, GPIO.IN)
        GPIO.setup(self.SPOTS_OUTPUT_PORT, GPIO.OUT)
        GPIO.setup(self.YES_BUTTON_PORT, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.NO_BUTTON_PORT, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.SOUND_INPUT_PORT, GPIO.BOTH)
        GPIO.add_event_callback(self.SOUND_INPUT_PORT, self.set_sound_switch)
        
        GPIO.output(self.SPOTS_OUTPUT_PORT, False)

    def set_sound_switch(self, *args, **kwargs):
        """
        Sets sound_switch to hight or low (True/False)
        by listening SOUND_INPUT_PORT
        """
        self.sound_level_high = GPIO.input(self.SOUND_INPUT_PORT)

    def sound_check(self):
        """
        Checks four times in 2 seconds
        that the sound level is still high
        then returns True. Else returns False
        """
        # print("sound test running")
        score = 0
        for _ in range(0, 3):
            if self.sound_level_high:
                score += 1
            sleep(1/4)
            # print("Score {0} at {1}".format(score, time()))
        if score == 3:
            return True
        else:
            return False

    def spots_on(self, switch = False):
        GPIO.output(self.SPOTS_OUTPUT_PORT, switch)