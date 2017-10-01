from time import sleep, time
from RPi import GPIO

class GPIOController(object):
    def __init__(self):
        self.SOUND_INPUT_PORT = 2
        self.sound_level_high = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SOUND_INPUT_PORT, GPIO.IN)
        GPIO.add_event_detect(self.SOUND_INPUT_PORT, GPIO.BOTH)
        GPIO.add_event_callback(self.SOUND_INPUT_PORT, self.set_sound_switch)

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
        for _ in range(0, 4):
            if self.sound_level_high:
                score += 1
            sleep(1/4)
            print("Score {0} at {1}".format(score, time()))
        if score == 4:
            return True
        else:
            return False
