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
from gui import GUIController
from snd_switch import SoundSwitch

GUI = GUIController()
GUI.mainloop()

sound_switch = SoundSwitch()

while True:
    if sound_switch.run_snd_test:
        GUI.show_frame_success()
