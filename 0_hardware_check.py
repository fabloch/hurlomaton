import sys
from shutil import copyfile
from time import sleep
from io import StringIO

import pyinotify
import requests
from PIL import Image, ImageEnhance
from controllers import GPIOController
from RPi import GPIO
from datetime import datetime, timedelta

#Test du static
print("Verification de l'électricité statique")
while GPIO.input(myGPIO.SOUND_INPUT_PORT) == 1:
    print("problème d'électricité statique")
    print("débranchez la machine quelques instants")
    sleep(1)

#test du bouton noir
print("appuyez sur le bouton noir")
while GPIO.input(myGPIO.NO_BUTTON_PORT) == 1:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("mauvais bouton detecté")
    elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        print("ok")
    sleep(0.5)

#test du bouton blanc
print("appuyez sur le bouton blanc")
while GPIO.input(myGPIO.YES_BUTTON_PORT) == 1:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("ok")
    elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        print("mauvais bouton detecté")
    sleep(0.5)


#test d'internet
print("comptez-vous utiliser internet ?")
while GPIO.input(myGPIO.NO_BUTTON_PORT) == 1 and GPIO.input(myGPIO.YES_BUTTON_PORT) == 1:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("Checking internet connection...")
        test_url = "https://www.google.com"
        response = requests.get(test_url)
        print(response)
        try:
            response.raise_for_status()
            print("Internet is working")
        except:
            print("!!!Internet is down, check connection!!!")
            sys.exit()

#test d'imprimante
print ("comptez-vous utiliser l'imprimante ?")
while GPIO.input(myGPIO.NO_BUTTON_PORT) == 1 and GPIO.input(myGPIO.YES_BUTTON_PORT) == 1:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("checking printer...")
        command = "sudo /user/bien/lp -d selphy_cp1200 Printer_Test_Page.png"
