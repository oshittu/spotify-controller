# the pico w can interact with spotify without my laptop as a middle-man.
# lets try it out

import machine
from machine import Pin, SPI
import st7789py as st7789
import spotipy
from spotipy.oauth2 import SpotifyOAuth
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

# hardware declarations
scl = Pin(18, Pin.OUT)  # SPI Synchro Clock, green
sda = Pin(19, Pin.OUT)  # Master Out Slave In (MOSI); send the data to the screen, blue
rst = Pin(16, Pin.IN)   # reset pin, white
dc = Pin(20, Pin.OUT)   # Data/Command, purple
cs = Pin(17, Pin.OUT)   # Chip select. Tells the display to listen to the SPI bus, yellow

red = Pin(15, Pin.IN)
blue = Pin(14, Pin.IN)

wif = 240
haiit = 320

spi = machine.SPI(
    0,
    baudrate=40000000,  # 40MHz for fast, crisp screen updates
    polarity=1,
    phase=1,
    sck=machine.Pin(18),
    mosi=machine.Pin(19)
)

display = st7789.ST7789(
    spi,
    wif,                # Width (Portrait)
    haiit,              # Height (Portrait)
    reset=rst,
    dc=dc,
    cs=cs,
    rotation=0          # 1 = Landscape (90 deg), 0 = Portrait (0 deg)
)

def draw_monkey(display, filename, x, y, width, height):
    row_bytes = width*2
    try:
        with open(filename, "rb") as f:
            for current_y in range(y, y+height):
                buffer = f.read(row_bytes)
                if not buffer:
                    break
                display.blit_buffer(buffer, x, current_y, width, 1)
    except OSError: 
         print(f"Error: Could not find or read file '{filename}'")

def swap_monkeys():
    if red.value():
        draw_monkey(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        sp.previous_track(device_id=None)
    elif blue.value():
        draw_monkey(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        sp.next_track(device_id=None)

while True:
    swap_monkeys()
    # print(f"jx: {jx.value()} \n jy: {jy.value()}")
    # time.sleep(1)

# display.fill(st7789.color565(0, 0, 0)