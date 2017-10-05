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
from time import sleep
from shortuuid import ShortUUID
from controllers import GUIController, GPIOController, PhotoController

if __name__ == '__main__':
    GUI = GUIController()
    GPIO = GPIOController()
    photo = PhotoController()

    GPIO.spots_on(True)
    sleep(2)
    GPIO.spots_on(False)

    while True:
        GUI.update()
        if GPIO.sound_check() or GUI.fake_success:
            photo.set_filepath(
                ShortUUID(
                    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                ).random(length=9)
            )
            GPIO.spots_on(True)
            # sleep(1)
            photo.run_all()
            GUI.show_success()
            GUI.update()
            # sleep(0.5)
            GPIO.spots_on(False)
            sleep(20)
            GUI.show_slideshow()
