"""
September 7th 2026
Push physical buttons to seek through spotify tracks

NOTES
    1. What spotipy command to seek through tracks - DONE
    2. How to http it                              - DONE
    3. Wifi connect the pico and http it           - DONE, but...
                                                    i wanna revise w a program that doesnt depend
                                                    on my laptop as an http host middleman

                                                    turns out middleman is needed cuz spotipy is heavy

September 28th 2026
imma figure it out       

SERVER = "http://192.168.1.78:5000"
"""

import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
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

DEVICES = {
    'Alexa': 'a5b7770f-2883-4188-b214-44a7905ab26f_amzn_1',
    'Google': '0025237bd65db2406276de6975a049ad',
    'tomilaptop': 'cb55267d486c2082da9fd19a923268626c116052',
    'tomiphone': '4faa5155ec7b663dfcfcea81c3671575a42eda5b',
}

COVERS_DIR = Path(__file__).with_name("covers")

@app.post("/next")
def nextTrack():
    sp.next_track(device_id=None)
    print("NEXT")

@app.post("/previous")
def previousTrack():
    sp.previous_track(device_id=None)
    print("BACK")

@app.post("/play/{device}")
def play(device: str):
    dId = DEVICES.get(device) # device ID
    if dId is None:
        raise HTTPException(status_code=404, detail="Unknown Spotify device")

    sp.transfer_playback(
        device_id = dId,
        force_play=True,
    )
    print(f"{device} is playing... listen and learn", flush=True)
    return {"ok": True, "device": device}

@app.get("/getPlaybackDump")
def getPlaybackDump():
    playback = sp.current_playback()
    if playback:
        return json.dumps(playback, indent=4)
    else:
        return "fail"

@app.get("/getAlbumName")
def getAlbumName():
    playback = sp.current_user_playing_track()
    album = playback["item"]["album"]["name"]
    return album

@app.get("/getAlbumID")
def getAlbumID():
    playback = sp.current_user_playing_track()
    albumID = playback["item"]["album"]["id"]
    return albumID

@app.get("/getCurrentSong")
def getCurrentSong():
    # playback = sp.current_user_playing_track()
    # song = playback["item"]["name"]
    # return song

    playing = sp.currently_playing()
    song = playing["item"]["name"]
    return song

@app.get("/getUser")
def getUser():
    player = sp.current_user()
    userID = player["display_name"]
    return userID

@app.get("/covers/{album_id}/{size}")
def getAlbumCover(album_id: str, size: int):
    if size not in (64, 200):
        raise HTTPException(status_code=404, detail="Unsupported cover size")

    cover_path = COVERS_DIR / "{}-{}.bin".format(album_id, size)
    if not cover_path.is_file():
        if album_id != getAlbumID():
            raise HTTPException(status_code=404, detail="Cover file not found")

        from convert_cover import convert_current_album

        convert_current_album()
        if not cover_path.is_file():
            raise HTTPException(status_code=404, detail="Cover file not found")

    expected_bytes = size * size * 2
    if cover_path.stat().st_size != expected_bytes:
        raise HTTPException(status_code=500, detail="Cover file has an invalid size")

    return FileResponse(cover_path, media_type="application/octet-stream")

@app.get("/getCoverURL64")
def getCoverURL64():
    playback = sp.current_user_playing_track()
    url64 = playback["item"]["album"]["images"][2]["url"]
    return url64

@app.get("/getCoverURL300")
def getCoverURL300():
    playback = sp.current_user_playing_track()
    url300 = playback["item"]["album"]["images"][1]["url"]
    return url300
