from time import sleep, time
from RPi import GPIO

class SoundSwitch(object):
    def __init__(self):
        self.sound_level_high = False
        self.GPIO_SND_IN = 2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_SND_IN, GPIO.IN)
        GPIO.add_event_detect(self.GPIO_SND_IN, GPIO.BOTH)
        GPIO.add_event_callback(self.GPIO_SND_IN, self.set_sound_level_high)

    def set_sound_level_high(self, *args, **kwargs):
        """
        Sets sound_level_high to True or False
        by listening GPIO port 16
        """
        self.sound_level_high = GPIO.input(self.GPIO_SND_IN)

    def run_snd_test(self):
        """
        Checks four times in 2 seconds
        that the sound level is still high
        and returns True. Else returns False
        """
        print("sound test running")
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