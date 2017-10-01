from time import sleep
from RPi import GPIO

class SoundSwitch(object):
    def __init__(self):
        self.sound_level_high = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(16, GPIO.BOTH)
        GPIO.add_event_callback(16, self.set_sound_level_high)

    def set_sound_level_high(self):
        """
        Sets sound_level_high to True or False
        by listening GPIO port 16
        """
        self.sound_level_high = GPIO.input(16)

    def run_snd_test(self):
        """
        Checks four times in 2 seconds
        that the sound level is still high
        and returns True. Else returns False
        """
        score = 0
        for _ in range(0, 4):
            if self.sound_level_high:
                score += 1
            sleep(1/4)
        return bool(score >= 4)
