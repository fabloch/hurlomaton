import sys
from shutil import copyfile
from time import sleep
from io import StringIO
import socket
import pyinotify
import requests
from PIL import Image, ImageEnhance
from controllers import GPIOController
from picamera import PiCamera
from datetime import datetime, timedelta
from RPi import GPIO
import subprocess as sub
import os

myGPIO = GPIOController()
blackTest = False
whiteTest = False
internetTest = False
imprimanteTest = False

#Test du static
print("\033[1;36;40m Verification de l'électricité statique..."'module' object has no attribute 'run')
while GPIO.input(myGPIO.SOUND_INPUT_PORT) == 1:
    print("\033[1;31;40m problème d'électricité statique\n")
    print("\033[1;31;40m débranchez la machine quelques instants")
    sleep(1)
print("\033[1;32;40m OK  \n")
sleep(1)

"""
#tempo pour l'allocation mémoire vidéo
print
"""
#Test du micro
print("\033[1;36;40m Verification du micro...")
print("\033[1;36;40m Hurlez s'il vous plaît")
while GPIO.input(myGPIO.SOUND_INPUT_PORT) == 0 or 0xFF == ord('m'):
    pass
print("\033[1;32;40m OK  \n")
sleep(1)

#Test de la caméra
print("\033[1;36;40m Verification de la caméra...")
try:
    camera = PiCamera()
    print("\033[1;32;40m OK\n")
except:
    print("\033[1;31;40m LA CAMÉRA N'EST PAS CONNECTÉE")
    sys.exit()

camera.close()

#test du bouton noir
print("\033[1;36;40m appuyez sur le bouton noir")
while blackTest == False :
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        sleep(1)
        blackTest = False
        print("\033[1;31;40m mauvais bouton detecté")
        print("\033[1;36;40m appuyez sur le bouton noir")
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
        print("\033[1;36;40m appuyez sur le bouton blanc")
    elif GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        sleep(1)
        whiteTest = True
        print("\033[1;32;40m OK  \n")
    sleep(0.5)
sleep(1)

#test d'internet
print("\033[1;36;40m comptez-vous utiliser internet ?")
while internetTest == False:
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            print("\033[1;36;40m vérification de la connection internet...")
            socket.create_connection(("www.google.com", 80))
            print("\033[1;32;40m OK  \n")
            sub.Popen("2_upload_watch")
            internetTest = True
        except OSError:
            print("\033[1;31;40m Connection à internet impossible, ré-esayer ?")
    elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        print("\033[1;32;40m SKIP \n")
        internetTest = True
        
sleep(1)

#test d'imprimante
print ("\033[1;36;40m comptez-vous utiliser l'imprimante ?")
while imprimanteTest == False :
    if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
        print("Impression de test...")
        command = "sudo /user/bien/lp -d selphy_cp1200 Printer_Test_Page.png"
        sub = subprocess.call(command, shell=True)
        print("\033[1;32;40m OK  \n")
        commandeImprimante = "python3 4_print_watch.py"
        sub = subprocess.call(commandeImprimante, shell=True)
        imprimanteTest = True
    elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
        print("\033[1;32;40m SKIP \n")
        imprimanteTest = True


print("\033[1;32;40m ****************************")
print("\033[1;32;40m *ALL SEEMS RIGHT, LET'S GO!*")
print("\033[1;32;40m ****************************\n")
