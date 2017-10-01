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
from shortuuid import ShortUUID
from controllers import GUIController, GPIOController, PhotoController

if __name__ == '__main__':
    GUI = GUIController()
    GPIO = GPIOController()
    photo = PhotoController()

    while True:
        GUI.update()
        if GPIO.sound_check() or GUI.fake_success:
            photo.set_filepath(
                ShortUUID(
                    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                ).random(length=9)
            )
            GUI.show_success()
            photo.run_all()
