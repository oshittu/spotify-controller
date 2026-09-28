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

def drawSymbol(display, symbol, x, y):
    mono_fb = framebuf.FrameBuffer(
            symbol["bytearray"],
            symbol["width"],
            symbol["height"],
            framebuf.MONO_HLSB
        )
    
    color_buf = bytearray(symbol["width"] * symbol["height"] * 2)
    color_fb = framebuf.FrameBuffer(color_buf, symbol["width"], symbol["height"], framebuf.RGB565)

    # swapping colours little endian to big
    # 1. Get the normal colors
    raw_bg = st7789.color565(0, 0, 0)
    raw_fg = st7789.color565(29, 185, 84)  # Spotify Green

    # 2. Swap the high byte and low byte so framebuf formats it correctly for SPI
    bg_color = (raw_bg >> 8) | ((raw_bg & 0xFF) << 8)
    fg_color = (raw_fg >> 8) | ((raw_fg & 0xFF) << 8)

    palette_buf = bytearray(4) # 2 pixels * 2 bytes
    palette = framebuf.FrameBuffer(palette_buf, 2, 1, framebuf.RGB565)
    palette.pixel(0, 0, bg_color) # Map all '0' bits to the background color
    palette.pixel(1, 0, fg_color) # Map all '1' bits to the foreground color

    color_fb.blit(mono_fb, 0, 0, -1, palette)
    display.blit_buffer(color_buf, x, y, symbol["width"], symbol["height"])
    
def drawScene(canvas):
    print

def drawImg(display, filename, x, y, width, height):
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


def show_monkeys():
    if HARDWARE.b0.value():
        drawImg(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b0")
    elif HARDWARE.b1.value():
        drawImg(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b1")
    elif HARDWARE.b2.value():
        drawImg(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b2")
    elif HARDWARE.b3.value():
        drawImg(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b3")
    elif HARDWARE.b4.value():
            drawImg(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
            print("b4")
    elif HARDWARE.b5.value():
        drawImg(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
        print("b5")

while True:
    if HARDWARE.b0.value():
        display.fill(st7789.BLACK)
    elif HARDWARE.b1.value():
        display.fill(st7789.RED)
    elif HARDWARE.b2.value():
        drawSymbol(display, SYMSCENE.symbols["sym_wifi"], 200, 3)