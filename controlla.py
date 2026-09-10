"""
September 7th 2026
Push physical buttons to seek through spotify tracks

NOTES
    1. What spotipy command to seek through tracks - DONE
    2. How to http it                              - DONE
    3. Wifi connect the pico and http it           - DONE, but...
                                                    i wanna revise w a program that doesnt depend
                                                    on my laptop as an http host middleman. this 
                                                    isnt that. see 'strongIndependentPico'
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import FastAPI, HTTPException
app = FastAPI()
import os
from dotenv import load_dotenv
load_dotenv()

# spotify details 
username = 'toeme'
# made up spotipy configs
scopes = "user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ["SPOTIFY_CLIENT_ID"],
    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
    scope="user-read-playback-state user-modify-playback-state",
))

@app.post("/next")
def nextTrack():
    sp.next_track(device_id=None)
    print("NEXT")

@app.post("/previous")
def previousTrack():
    sp.previous_track(device_id=None)
    print("BACK")