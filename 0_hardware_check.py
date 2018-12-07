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

myGPIO = GPIOController()
blackTest = False
whiteTest = False

#Test du static
print("\033[1;36;40m Verification de l'électricité statique...")
while GPIO.input(myGPIO.SOUND_INPUT_PORT) == 1:
    print("\033[1;31;40m problème d'électricité statique\n")
    print("\033[1;36;40m débranchez la machine quelques instants")
    sleep(1)
print("\033[1;32;40m OK  \n")
sleep(1)

#test du bouton noir
print("\033[1;36;40m appuyez sur le bouton noir")
while blackTest == False :
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        sleep(1)
        blackTest = False
        print("\033[1;31;40m mauvais bouton detecté")
    elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        sleep(1)
        blackTest = True
        print("\033[1;32;40m OK  \n")
    sleep(0.5)
sleep(1)

#test du bouton blanc
print("\033[1;36;40m appuyez sur le bouton blanc")
while whiteTest == False :
    if GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        sleep(1)
        whiteTest = False
        print("\033[1;31;40m mauvais bouton detecté")
    elif GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        sleep(1)
        whiteTest = True
        print("\033[1;32;40m OK  \n")
    sleep(0.5)
sleep(1)

#test d'internet
print("\033[1;36;40m comptez-vous utiliser internet ?")
while GPIO.input(myGPIO.NO_BUTTON_PORT) == 1 and GPIO.input(myGPIO.YES_BUTTON_PORT) == 1:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("Checking internet connection...")
        test_url = "https://www.google.com"
        response = requests.get(test_url)
        print(response)
        try:
            response.raise_for_status()
            print("\033[1;32;40m OK  \n")
        except:
            print("\033[1;31;40m !!!Internet is down, check connection!!!")
            sys.exit()
    elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        print("\033[1;32;40m SKIP \n")
        
sleep(1)

"""
#test d'imprimante
print ("\033[1;36;40m comptez-vous utiliser l'imprimante ?")
while GPIO.input(myGPIO.NO_BUTTON_PORT) == 1 and GPIO.input(myGPIO.YES_BUTTON_PORT) == 1:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("checking printer...")
        command = "sudo /user/bien/lp -d selphy_cp1200 Printer_Test_Page.png"
"""
