import threading
from datetime import datetime, timedelta

import RPi.GPIO as GPIO

CONST = {
    "CHALLENGE_TIME_MS": 1500,
    "FAIL_TIME_MS": 2000,
    "SUCCESS_TIME_MS": 5000,
    "CHOICE_TIME_MS": 20000,
    "PUBLISHING_TIME_MS": 20000,
    "TICK_TIME_MS": 5000,
    "SOUND_INPUT_PORT": 2,
    "SPOTS_OUTPUT_PORT": 4,
    "YES_BUTTON_PORT": 18,
    "NO_BUTTON_PORT": 23,
    "IDLE_DELAY_MS": 5000,
    "PRINTER_1": "Canon_SELPHY_CP1200",
    "PRINTER_2": "Canon_CP1000",
    "EVENT_NAME": "2022cm2",
}


def time_since(some_datetime):
    return datetime.now() - some_datetime


def is_after(ms_duration, some_timedelta):
    return some_timedelta >= timedelta(milliseconds=ms_duration)


def format_time(time, filename=False):
    if filename:
        return time.strftime("%H%M%S%f")
    return time.strftime("%H:%M:%S:%f")


def set_now():
    return datetime.now()


def add_ms(milliseconds, time):
    return time + timedelta(milliseconds=milliseconds)


class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge="both", bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime) / 1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
            (pinval == 0 and self.lastpinval == 1)
            and (self.edge in ["falling", "both"])
        ) or (
            (pinval == 1 and self.lastpinval == 0) and (self.edge in ["rising", "both"])
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()
