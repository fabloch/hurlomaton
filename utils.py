from datetime import datetime, timedelta

CONST = {
    "CHALLENGE_TIME_MS": 1500,
    "FAIL_TIME_MS": 2000,
    "SUCCESS_TIME_MS": 5000,
    "CHOICE_TIME_MS": 20000,
    "PUBLISHING_TIME_MS": 70000,
    "TICK_TIME_MS": 5000,
    "SOUND_INPUT_PORT": 2,
    "SPOTS_OUTPUT_PORT": 4,
    "YES_BUTTON_PORT": 18,
    "NO_BUTTON_PORT": 23,
    "MEDIA_FOLDER": "testing",
    "IDLE_DELAY_MS": 5000,
    "PRINTER_NAME": "Canon_SELPHY_CP1200",
    "EVENT_NAME": "testing",
}


def time_since(some_datetime):
    return datetime.now() - some_datetime


def is_after(ms_duration, some_timedelta):
    return some_timedelta >= timedelta(milliseconds=ms_duration)


def format_time(time):
    return time.strftime("%H:%M:%S:%f")


def set_now():
    return datetime.now()


def add_ms(milliseconds, time):
    return time + timedelta(milliseconds=milliseconds)
