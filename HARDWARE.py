import machine
from machine import Pin, SPI
import st7789
#import st7789py as st7789
import time

scWidth = 240   # screen width
scHeight = 320

# hardware declarations
scl = Pin(18, Pin.OUT)  # SPI Synchro Clock, green
sda = Pin(19, Pin.OUT)  # Master Out Slave In (MOSI); send the data to the screen, blue
rst = Pin(16, Pin.IN)   # reset pin, white
dc = Pin(20, Pin.OUT)   # Data/Command, purple
cs = Pin(17, Pin.OUT)   # Chip select. Tells the display to listen to the SPI bus, yellow

# buttons r numbered left to right, top row then bottom row
b0 = Pin(10, Pin.IN, machine.Pin.PULL_DOWN) # top left corner button
b1 = Pin(11, Pin.IN, machine.Pin.PULL_DOWN)
b2 = Pin(12, Pin.IN, machine.Pin.PULL_DOWN) 
b3 = Pin(13, Pin.IN, machine.Pin.PULL_DOWN) 
b4 = Pin(14, Pin.IN, machine.Pin.PULL_DOWN)
b5 = Pin(15, Pin.IN, machine.Pin.PULL_DOWN)

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
    scWidth,                # Width (Portrait)
    scHeight,              # Height (Portrait)
    reset=rst,
    dc=dc,
    cs=cs,
    rotation=0          # 1 = Landscape (90 deg), 0 = Portrait (0 deg)
)

def testButtons():
    print(f"b0: {b0.value()} \nb1: {b1.value()} \nb2: {b2.value()} \nb3: {b3.value()} \nb4: {b4.value()} \nb5: {b5.value()}\n")
    time.sleep(1)