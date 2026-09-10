# ai wrote this. i couldnt find a library...
# Save this exact code block entirely inside a file named st7789py.py on your Pico
import time
import ustruct
import machine

def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

class ST7789:
    def __init__(self, spi, width, height, reset, dc, cs=None, backlight=None, rotation=0):
        self.spi = spi
        self.width = width
        self.height = height
        self.reset = reset
        self.dc = dc
        self.cs = cs
        self.backlight = backlight
        self.rotation = rotation
        # self.hard_reset()
        self.init()

    def init(self):
        # Driver basic initialization routine
        for cmd, data, delay in [
            (0x01, b"", 150),          # SWRESET
            (0x11, b"", 500),          # SLPOUT
            (0x3A, b"\x55", 10),       # COLMOD (16-bit color)
            (0x21, b"", 10),           # INVON (Inversion on)
            (0x13, b"", 10),           # NORON
            (0x29, b"", 100),          # DISPON
        ]:
            self.write(cmd, data)
            if delay > 0:
                time.sleep_ms(delay)
                
    def write(self, command, data=None):
        if self.cs: self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([command]))
        if data:
            self.dc.on()
            self.spi.write(data)
        if self.cs: self.cs.on()

    def fill(self, color):
        buffer = bytearray(self.width * self.height * 2)
        high = color >> 8
        low = color & 0xFF

        for index in range(0, len(buffer), 2):
            buffer[index] = high
            buffer[index + 1] = low

        self.blit_buffer(
            buffer,
            0,
            0,
            self.width,
            self.height
        )

    def blit_buffer(self, buffer, x, y, width, height):
        # Sets window area and dumps binary buffer data
        self.write(0x2A, ustruct.pack(">HH", x, x + width - 1))
        self.write(0x2B, ustruct.pack(">HH", y, y + height - 1))
        self.write(0x2C, buffer)
