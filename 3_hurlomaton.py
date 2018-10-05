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
import os

def capture_photo():
    photo.set_filepath(
        ShortUUID(
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ).random(length=9)
    )
#    myGPIO.spots_on(True)
    sleep(0.3)
    photo.capture()
    print("Capturing " + photo.pathname)
    GUI.show_success()
    sleep(0.3)
    myGPIO.spots_on(False)
    # sleep(10)
    # GUI.show_slideshow()

if __name__ == '__main__':

    GUI = GUIController()

    myGPIO = GPIOController()
    photo = PhotoController()

    myGPIO.spots_on(True)
    sleep(2)
    myGPIO.spots_on(False)

    test_start_time = None
    success_start_time = None
    test_print = False
    slide_print = False

    """
    LOOP----1---X-------2-------3--------->
            |   |       |       |
            le son est high     |
            on donne une valeur test_start_time
                |       |       |
                |       now() - test_start_time >= 2 secondes
                |       on donne une valeur a success_start_time
                |       on affiche les diapos success
                |               |
                |               |
                |               now() - success_start_time >= 10 secondes
                |               on reset tout
                |               on affiche les diapos idle
                |
                le son passe low avant d'atteindre les 2 secondes
                on reset test_start_time
    """
    while True:
        if GPIO.input(myGPIO.SOUND_INPUT_PORT) == 1 or success_start_time:
            """
            [1] Le sound level est HIGH
                OU success_start_time est True
            """
            if not test_start_time:
                """
                c'est la premiere boucle
                test_start_time n'existe pas ?
                alors on l'initialise
                """
                print("[1] Init test_start_time")
                test_start_time = datetime.now()
            else:
                """
                entre [1] et [3]
                test_start_time existe,
                donc nous allons comparer le timedelta
                entre now() et test_start_time
                """
                test_time_delta = datetime.now() - test_start_time
                if test_time_delta >= timedelta(microseconds=1000000):
                    """
                    [2] test_time_delta est >= 2 secondes
                    On est dans la boucle success
                    """
                    if not success_start_time:
                        """
                        success_start_time n'existe pas ?
                        alors on l'initialise
                        on lance la capture
                        on lance les ecrans success
                        """
                        print("[2] success")
                        print("[2] init success_start_time")
                        success_start_time = datetime.now()
                        capture_photo()
                        GUI.show_success()

                    else:
                        """
                        entre [2] et [3]
                        success_start_time existe,
                        donc nous allons comparer le timedelta
                        entre now() et success_start_time
                        """
                        success_time_delta = datetime.now() - success_start_time
                        if success_time_delta >= timedelta(seconds=3) and success_time_delta <= timedelta(seconds=4) and not slide_print:
                            print("getting images")
                            GUI.list_print()
                            slide_print = True

                        


                        if (success_time_delta >= timedelta(seconds=6) and success_time_delta <= timedelta(seconds=16)
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

                        elif (success_time_delta >= timedelta(seconds=16)
                              or test_print):
                            '''
                            success _time_delta est >= à 16 secondes
                            ou l'utilisateur à fait ses choix pour l'upload et l'impression
                            on affiche donc le slideshow
                            '''
                            GUI.show_slideshow()
                            test_start_time = None
                            success_start_time = None
                            test_print = False
                            slide_print=False
                            os.remove("/home/pi/dev/hurlomaton/media/print/fond-print1.jpg")
                            os.remove("/home/pi/dev/hurlomaton/media/print/fond-print2.jpg")
                            
        else:
            """
            [x] Si GPIO == 0 on reset start
            """
            if test_start_time:
                print("[x] reset test_start_time")
                test_start_time = None
        GUI.update()
