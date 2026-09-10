import machine
import time
from machine import Pin, SPI
import st7789py as st7789

red = Pin(15, Pin.IN)
blue = Pin(14, Pin.IN)

while True:
    print(f"red: {red.value()}        blue: {blue.value()}")
    time.sleep(0.35)