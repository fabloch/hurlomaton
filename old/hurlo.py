"""
Main Hurlomaton python program
- launches the slideshow
- listen to the GPIO number ###
- if the GPIO is True for two seconds...
    - launches the spots on GPIO ###
    - wait 0.5s
    - captures an image
    - shows success screens
        - screen 1: Well done!
        - screen 2: The picture
        - sreeen 3: Thank you!
"""
from datetime import datetime, timedelta
from time import sleep
from controllers import GUIController, GPIOController, PhotoController
from shortuuid import ShortUUID
from RPi import GPIO
from PIL import Image, ImageTk, ImageOps
from utils import CONST
import os

def capture_photo():
    photo.set_filepath(
        ShortUUID(
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ).random(length=9)
    )
    myGPIO.spots_on(True)
    sleep(0.3)
    photo.capture()
    print("Capturing " + photo.pathname)
    GUI.show_success()
    sleep(0.3)
    myGPIO.spots_on(False)
    # sleep(10)
    # GUI.show_slideshow()

if __name__ == '__main__':
    try:
        GUI = GUIController()

        myGPIO = GPIOController()
        photo = PhotoController()

        myGPIO.spots_on(True)
        sleep(2)
        myGPIO.spots_on(False)

        scream_start = None
        capture_start = None
        test_print = False
        slide_print = False

        """
        LOOP----1---X-------2-------3--------->
                |   |       |       |
                le son est high     |
                on donne une valeur scream_start
                    |       |       |
                    |       now() - scream_start >= CHALLENGE_TIME_MS (2 sec ?)
                    |       on donne une valeur a capture_start
                    |       on affiche les diapos success
                    |               |
                    |               |
                    |               now() - capture_start >= 10 secondes
                    |               on reset tout
                    |               on affiche les diapos idle
                    |
                    le son passe low avant d'atteindre les 2 secondes
                    on reset scream_start
        """
        while True:
            if GPIO.input(myGPIO.SOUND_INPUT_PORT) == 1 or capture_start:
                """
                [1] Le sound level est HIGH
                    OU capture_start est True
                """
                if not scream_start:
                    """
                    c'est la premiere boucle
                    scream_start n'existe pas ?
                    alors on l'initialise
                    """
                    print("[1] Init scream_start")
                    scream_start = datetime.now()
                else:
                    """
                    entre [1] et [3]
                    scream_start existe,
                    donc nous allons comparer le timedelta
                    entre now() et scream_start
                    """
                    scream_duration = datetime.now() - scream_start
                    if scream_duration >= timedelta(milliseconds=CONST["CHALLENGE_TIME_MS"]):
                        """
                        [2] scream_duration est >= CHALLENGE_TIME_MS
                        On est dans la boucle success
                        """
                        if not capture_start:
                            """
                            capture_start n'existe pas ?
                            alors on l'initialise
                            on lance la capture
                            on lance les ecrans success
                            """
                            print("[2] success")
                            print("[2] init capture_start")
                            capture_start = datetime.now()
                            capture_photo()
                            # GUI.show_success()

                        else:
                            """
                            entre [2] et [3]
                            capture_start existe,
                            donc nous allons comparer le timedelta
                            entre now() et capture_start
                            """
                            capture_duration = datetime.now() - capture_start
                            if capture_duration >= timedelta(seconds=3) and capture_duration <= timedelta(seconds=4) and not slide_print:
                                print("getting images")
                                GUI.list_print()
                                slide_print = True




                            if (capture_duration >= timedelta(seconds=6) and capture_duration <= timedelta(seconds=16)
                                  and slide_print and not test_print):
                                """
                                succes_time_delta est  >= à 6 secondes et <= à 16 secondes
                                ou l'utilisateur à fait son choix pour l'upload mais pas l'impression
                                on lui laisse donc 10s pour faire un choix
                                """
                                GUI.show_print()

                                if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
                                    sleep(0.5)
                                    print("print: YES")
                                    test_print = True

                                elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
                                    sleep(0.5)
                                    print("print: NO")
                                    test_print = True

                            elif (capture_duration >= timedelta(seconds=16)
                                  or test_print):
                                '''
                                success _time_delta est >= à 16 secondes
                                ou l'utilisateur à fait ses choix pour l'upload et l'impression
                                on affiche donc le slideshow
                                '''
                                GUI.show_slideshow()
                                scream_start = None
                                capture_start = None
                                test_print = False
                                slide_print=False
                                os.remove("/home/pi/dev/hurlomaton/media/print/fond-print1.jpg")
                                os.remove("/home/pi/dev/hurlomaton/media/print/fond-print2.jpg")

            else:
                """
                [x] Si GPIO == 0 on reset start
                """
                if scream_start:
                    print("[x] reset scream_start")
                    scream_start = None
            GUI.update()

    except KeyboardInterrupt:
        print("Keyboard exit.")

    except Exception as e:
        print("Error:", str(e))

    finally:
        GPIO.cleanup()
