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
    826674905872: {'song': 'spotify:album:1o59UpKw81iHR0HPiSkJR0', 'shuffle': False},
    1032531346238: {'song': 'spotify:album:5AEDGbliTTfjOB8TSm1sxt', 'shuffle': False},
    2041119699: {'song': 'spotify:album:3lS1y25WAhcqJDATJK70Mq', 'shuffle': False},
    620231197522: {'song': 'spotify:album:6kZ42qRrzov54LcAk4onW9', 'shuffle': False},
    689573397481: {'song': 'spotify:album:4hDok0OAJd57SGIT8xuWJH', 'shuffle': False},
    1033002943414: {'song': 'spotify:album:6AORtDjduMM3bupSWzbTSG', 'shuffle': False},
    757856600838: {'song': 'spotify:album:1pzvBxYgT6OVwJLtHkrdQK', 'shuffle': False},
    964367287214: {'song': 'spotify:album:1NAmidJlEaVgA3MpcPFYGq', 'shuffle': False},
    2059731900: {'song': 'spotify:album:6DEjYFkNZh67HP7R9PSZvv', 'shuffle': False},
    277222785804: {'song': 'spotify:album:6CczqhUdYOH4qLSDnN3zkg', 'shuffle': False},
    964065231697: {'song': 'spotify:album:6BUPtXbb2tspYnkVdg5Ef7', 'shuffle': False},
    139146232709: {'song': 'spotify:album:3gF9KIynrJaC80HbVayPMx', 'shuffle': False},
    963696001857: {'song': 'spotify:album:1xJHno7SmdVtZAtXbdbDZp', 'shuffle': False},
    413571089387: {'song': 'spotify:album:1kCHru7uhxBUdzkm4gzRQc', 'shuffle': False},
    414743397201: {'song': 'spotify:album:14hC5eBiPUxdPa90eCzwrR', 'shuffle': False},
    277086405475: {'song': 'spotify:playlist:5qvEvL5VYNxMi7Q7PWIS6u', 'shuffle': False},
    2040792030: {'song': 'spotify:playlist:6ZIftcLT2xNsCOWaTdCdfs', 'shuffle': False},
    1033051046865: {'song': 'spotify:playlist:4xsTCcceRE7HEBhtpt2zKP', 'shuffle': False},
    620482593601: {'song': 'spotify:playlist:25HjzG4TGTUzywEaOpB969', 'shuffle': False},
    895159239454: {'song': 'spotify:playlist:2J8GVBFf9ZpzuZFsN5qym5', 'shuffle': False},
    826775307034: {'song': 'spotify:album:2g4aJTa5ejGpp0O0GKzWAQ', 'shuffle': False},
    826590823184: {'song': 'spotify:album:1pb3je8gXTs5dpRRTKhHRC', 'shuffle': False},
    552082015150: {'song': 'spotify:playlist:6kerovxFzKzlnKGkbiKRnm', 'shuffle': False},
    345739101060: {'song': 'spotify:album:2c7gFThUYyo2t6ogAgIYNw', 'shuffle': False}
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

                sp.start_playback(device_id=DEVICE_ID, uris=[CARD_URI_DICT[id]['song']]) # play the song/album
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