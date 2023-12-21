#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

while True:
    try:
        print("Waiting for you to scan an RFID sticker/card")
        id = reader.read()[0]
        print("The ID for this card is: ", id)
    except KeyboardInterrupt:
        print("Exiting the program")
        break
    
GPIO.cleanup()