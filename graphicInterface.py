"""
Goal: Make a decent interface

at the minimum: describe controls "skipped to next song", "playback paused", etc

> Display album cover?
> Make it like an iPod?
""" 
import machine
from machine import Pin, SPI
#import st7789py as st7789
import st7789
import time
import HARDWARE, SYMSCENE
import framebuf

display = HARDWARE.display
display.init()
wif = HARDWARE.scWidth
haiit = HARDWARE.scHeight

def show_monkeys():
    if HARDWARE.b0.value():
        SYMSCENE.drawImg(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b0")
    elif HARDWARE.b1.value():
        SYMSCENE.drawImg(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b1")
    elif HARDWARE.b2.value():
        SYMSCENE.drawImg(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b2")
    elif HARDWARE.b3.value():
        SYMSCENE.drawImg(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b3")
    elif HARDWARE.b4.value():
        SYMSCENE.drawImg(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b4")
    elif HARDWARE.b5.value():
        SYMSCENE.drawImg(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b5")

while True:
    if HARDWARE.b0.value():
        display.fill(st7789.BLACK)
    elif HARDWARE.b1.value():
        display.fill(st7789.RED)
    elif HARDWARE.b2.value():
        SYMSCENE.drawSymbol(display, SYMSCENE.symbols["sym_wifi"], 200, 3)