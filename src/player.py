#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
# import env variables
from dotenv import load_dotenv

DEVICE_ID=dotenv.get('DEVICE_ID')
CLIENT_ID=dotenv.get('CLIENT_ID')
CLIENT_SECRET=dotenv.get('CLIENT_SECRET')

# dictionary of card values and their corresponding song / album URIs
CARD_URI_DICT = {
    'RFID-CARDVALUE-1': { # the card value, should be a number not a string
        'song': 'spotify:track:0000',
        'shuffle': False
    },
    'RFID-CARDVALUE-2': {
        'song': 'spotify:album:0000',
        'shuffle': True
    }
    # continue adding as many card values and URIs as you want
}

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://localhost:8080",
                scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is: ",id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

            # if the card value is in the dictionary, play the corresponding song/album
            if (id in CARD_URI_DICT):
                print("Playing song/album...") 

                sp.start_playback(device_id=DEVICE_ID, uris=[CARD_URI_DICT[id]]) # play the song/album
                sp.shuffle(state=CARD_URI_DICT[id]['shuffle']) # shuffle if the card value is set to shuffle

                sleep(2)

            else:
                print("Unknown card, please try a different one.")

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        # eventually handle if the device id is not active / changes, then update the DEVICE_ID variable
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()