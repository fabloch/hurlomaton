from time import sleep

# from PIL import Image, ImageTk, ImageOps
from controllers import UIController

# from controllers import NoUIController
from controllers import CaptureController
from controllers import IOController
from controllers import PublishController
from utils import CONST, is_after, time_since, format_time, set_now

# import os
from tkinter import TclError

printer_down = False

scream_start = False
fail_start = False
success_start = False
choice_start = False
publish_start = False
bug_mode = False
tick = False
print_on_1 = True

UI = UIController()

IO = IOController()
capture = CaptureController()
publish = PublishController()


if __name__ == "__main__":

    try:
        # IO.spots_on(True)
        # sleep(2)
        # IO.spots_on(False)

        def reset():
            global scream_start, fail_start, success_start
            global choice_start, publish_start, bug_mode, tick
            scream_start = None
            fail_start = None
            success_start = None
            choice_start = None
            publish_start = None
            bug_mode = None
            tick = None
            IO.yes_btn_pressed = False
            IO.no_btn_pressed = False

        def show_idle():
            global UI
            reset()
            UI.show_idle()

        def show_screaming():
            global UI
            global scream_start
            scream_start = set_now()
            UI.show_screaming()

        def show_fail():
            global UI
            global fail_start
            reset()
            fail_start = set_now()
            UI.show_fail()

        def show_success():
            global capture, IO, UI
            global success_start
            IO.spots_on(True)
            sleep(0.3)
            capture.take_photo()
            sleep(0.3)
            UI.show_success()
            IO.spots_on(False)
            capture.process()

            reset()
            success_start = set_now()
            UI.show_success()

        def show_choice():
            global UI
            global choice_start
            reset()
            choice_start = set_now()
            UI.show_choice()

        def show_publishing():
            global UI
            global publish_start, tick
            global print_on_1
            reset()
            publish_start = set_now()
            tick = set_now()
            UI.show_publishing()
            publish.start_print(print_on_1)
            print_on_1 = not print_on_1

        def show_bug():
            global UI
            global bug_mode
            reset()
            UI.show_bug()
            bug_mode = True

        while True:
            states = [
                scream_start,
                fail_start,
                success_start,
                choice_start,
                publish_start,
                bug_mode,
                tick,
            ]

            if not any(states) and IO.yes_btn_pressed:
                show_publishing()

            if bug_mode:
                if IO.yes_btn_pressed:
                    show_publishing()

                if IO.no_btn_pressed:
                    show_idle()

            """ start screaming """
            if IO.sound_level_high and not any(states):
                show_screaming()
                print("scream_start", format_time(scream_start))

            """ end of screaming => fail """
            if not IO.sound_level_high and scream_start:
                show_fail()
                print("fail_start", format_time(fail_start))

            """ end of fail => idle """
            if fail_start:
                fail_duration = time_since(fail_start)
                if is_after(CONST["FAIL_TIME_MS"], fail_duration):
                    show_idle()

            """ end of screaming => success """
            if IO.sound_level_high and scream_start:
                scream_duration = time_since(scream_start)
                if is_after(CONST["CHALLENGE_TIME_MS"], scream_duration):
                    show_success()
                    print("success_start", format_time(success_start))

            """ end of success => choice """
            if success_start:
                success_duration = time_since(success_start)
                if is_after(CONST["SUCCESS_TIME_MS"], success_duration):
                    show_choice()
                    print("choice_start", format_time(choice_start))

            """ end of choice """
            if choice_start:
                choice_duration = time_since(choice_start)
                """ => idle # time is up """
                if is_after(CONST["CHOICE_TIME_MS"], choice_duration):
                    show_idle()
                    print("too long to choose, restarting")

                """ => publishing # yes button pressed """
                if IO.yes_btn_pressed:
                    show_publishing()
                    print("publish_start", format_time(publish_start))

                """ => idle # no button pressed """
                if IO.no_btn_pressed:
                    capture.clean_ramdisk()
                    show_idle()

            """ end of publishing """
            if publish_start:
                publish_duration = time_since(publish_start)

                """ => bug # time is up """
                if is_after(CONST["PUBLISHING_TIME_MS"], publish_duration):
                    show_idle()
                    # print("print time is up")

            # """ checking printer every 5 seconds """
            # if tick:
            #     tick_duration = time_since(tick)
            #     if is_after(CONST["TICK_TIME_MS"], tick_duration):
            #         if not publish.check_print_done():
            #             tick = add_ms(CONST["TICK_TIME_MS"], tick)
            #         else:
            #             show_idle()

            UI.update()

    except KeyboardInterrupt:
        print("Keyboard exit.")

    except TclError:
        pass

    finally:
        IO.cleanup()
