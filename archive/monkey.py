# control monkeys with a joystick

import machine
import time
from machine import Pin, SPI
import st7789py as st7789

#SERVER = "http://192.168.1.78:5000"

# hardware declarations
scl = Pin(18, Pin.OUT)  # SPI Synchro Clock, green
sda = Pin(19, Pin.OUT)  # Master Out Slave In (MOSI); send the data to the screen, blue
rst = Pin(16, Pin.IN)   # reset pin, white
dc = Pin(20, Pin.OUT)   # Data/Command, purple
cs = Pin(17, Pin.OUT)   # Chip select. Tells the display to listen to the SPI bus, yellow

# stuck the joystick directly into the breakboard (awful)
jx = Pin(8, Pin.IN)     # gray
jy = Pin(9, Pin.IN)     # white
jsw = Pin(4, Pin.IN)    # orange

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
    if jy.value() == 0:
        draw_monkey(display, "monkey-thinking-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
    elif jy.value() == 1:
        draw_monkey(display, "monkey-thought-240x320.bin", x = 0, y = 0, width = wif, height = haiit)
    

while True:
    swap_monkeys()
    # print(f"jx: {jx.value()} \n jy: {jy.value()}")
    # time.sleep(1)

# display.fill(st7789.color565(0, 0, 0)