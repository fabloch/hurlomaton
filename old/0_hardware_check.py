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

try:
    myGPIO = GPIOController()
    blackTest = False
    whiteTest = False
    internetTest = False
    imprimanteTest = False
    printTestFile = False


    #Test du static
    print("\033[1;36;40m Vérification de l'électricité statique...")
    while GPIO.input(myGPIO.SOUND_INPUT_PORT) == 1:
        print("\033[1;31;40m problème d'électricité statique\n")
        print("\033[1;31;40m débranchez la machine quelques instants")
        sleep(1)
    print("\033[1;32;40m OK  \n")
    sleep(1)


    #Test du micro
    print("\033[1;36;40m Vérification du micro...")
    print("\033[1;36;40m Hurlez s'il vous plaît")
    while GPIO.input(myGPIO.SOUND_INPUT_PORT) == 0 or 0xFF == ord('m'):
        pass
    print("\033[1;32;40m OK  \n")
    sleep(1)

    #Test de la caméra
    print("\033[1;36;40m Vérification de la caméra...")
    try:
        camera = PiCamera()
        print("\033[1;32;40m OK\n")
    except:
        print("\033[1;31;40m LA CAMÉRA N'EST PAS CONNECTÉE")
        sys.exit()

    camera.close()

    #test du bouton noir
    print("\033[1;36;40m Appuyez sur le bouton NON (noir)")
    while blackTest == False :
        if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
            sleep(1)
            blackTest = False
            print("\033[1;31;40m Mauvais bouton detecté")
            print("\033[1;36;40m Appuyez sur le bouton NON (noir)")
        elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
            sleep(1)
            blackTest = True
            print("\033[1;32;40m OK  \n")
        sleep(0.5)
    sleep(1)

    #test du bouton blanc
    print("\033[1;36;40m Appuyez sur le bouton OUI (blanc)")
    while whiteTest == False :
        if GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
            sleep(1)
            whiteTest = False
            print("\033[1;31;40m Mauvais bouton detecté")
            print("\033[1;36;40m Appuyez sur le bouton OUI (blanc)")
        elif GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
            sleep(1)
            whiteTest = True
            print("\033[1;32;40m OK  \n")
        sleep(0.5)
    sleep(1)

    #test d'internet
    print("\033[1;36;40m Comptez-vous utiliser internet ?")
    while internetTest == False:
        if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
            try:
                # connect to the host -- tells us if the host is actually
                # reachable
                print("\033[1;36;40m Vérification de la connection internet...")
                socket.create_connection(("www.google.com", 80))
                print("\033[1;32;40m OK  \n")
                Internet = "python3 2_upload_watch.py & "
                internetTest = True
            except OSError:
                print("\033[1;31;40m Connection à internet impossible, vérifiez le branchement et appuyez sur")
                print("\033[1;31;40m     OUI (blanc) pour réessayer")
                print("\033[1;31;40m     NON (noir) pour annuler")
        elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
            print("\033[1;32;40m SKIP \n")
            Internet = ""
            internetTest = True
            
    sleep(1)

    #test d'imprimante
    print ("\033[1;36;40m Comptez-vous utiliser l'imprimante ?")
    while imprimanteTest == False :
        if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
            sleep(1)
            print ("\033[1;36;40m     OK. Imprimer une page de test ?")
            while printTestFile == False:
                if GPIO.input(myGPIO.YES_BUTTON_PORT) == 0:
                    print("Impression de test...")
                    command = "sudo lp -d Canon_SELPHY_CP1200 Printer_Test_page.png"
                    sub.call(command, shell=True)
                    printTestFile = True
                elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
                    printTestFile = True
            print("\033[1;32;40m OK  \n")
            Imprimante = "python3 4_print_watch.py & "
            imprimanteTest = True
        elif GPIO.input(myGPIO.NO_BUTTON_PORT) == 0:
            print("\033[1;32;40m SKIP \n")
            Imprimante = ""
            imprimanteTest = True


    print("\033[1;32;40m *******************************")
    print("\033[1;32;40m * TOUT EST COOl, C'EST PARTI! *")
    print("\033[1;32;40m *******************************\n")

    GPIO.cleanup()
    commande = "python3 1_crop_watch.py & " + Internet + Imprimante + "python3 3_hurlomaton.py"
    sub.call(commande, shell=True)

except KeyboardInterrupt:
    print("Keyboard exit.")

except Exception as e:
    print("Error:", str(e))

finally:
    GPIO.cleanup()
