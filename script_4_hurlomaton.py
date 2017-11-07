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
from shortuuid import ShortUUID
from controllers import GUIController, GPIOController, PhotoController
from RPi import GPIO

def capture_photo():
    photo.set_filepath(
        ShortUUID(
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ).random(length=9)
    )
    myGPIO.spots_on(True)
    # sleep(1)
    photo.capture()
    print("Capturing " + photo.pathname)
    GUI.show_success()
    GUI.update()
    # sleep(0.5)
    myGPIO.spots_on(False)
    # sleep(10)
    # GUI.show_slideshow()

if __name__ == '__main__':

    SOUND_INPUT_PORT = 2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUND_INPUT_PORT, GPIO.IN)

    GUI = GUIController()
    myGPIO = GPIOController()
    photo = PhotoController()

    myGPIO.spots_on(True)
    sleep(2)
    myGPIO.spots_on(False)

    start_time = None

    while True:
        GUI.update()
        if GPIO.input(SOUND_INPUT_PORT) == 1:
            print("Sound detected")
            if start_time:
                """
                start existe, donc on est 
                """
                time_since_start = datetime.now() - start_time
                print(time_since_start)
                if time_since_start >= timedelta(microseconds=2000000):
                    print("Success")
                
            else:
                start_time = datetime.now()
        else:
            """
            Si GPIO == 0 on reset start
            """
            start_time = None

# or GUI.fake_success
