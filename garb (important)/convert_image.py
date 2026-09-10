# Convert a PNG into raw RGB565 bytes for the Pico ST7789 display.
#
# First-time setup on the computer:
#     python -m pip install Pillow
#
# Run from this folder:
#     python convert_image.py input.png output.bin
#
# Example:
#     python convert_image.py monkey-thought.png monkey-thought-240x320.bin
#
# The output must be copied to the Pico. It should be exactly 153600 bytes
# because the display is 240 x 320 pixels and each RGB565 pixel uses 2 bytes.

from pathlib import Path
import argparse

from PIL import Image


DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320
BYTES_PER_PIXEL = 2


def rgb888_to_rgb565(red, green, blue):
    return ((red & 0xF8) << 8) | ((green & 0xFC) << 3) | (blue >> 3)


def convert_image(source_path, output_path):
    expected_size = DISPLAY_WIDTH * DISPLAY_HEIGHT * BYTES_PER_PIXEL

    with Image.open(source_path) as image:
        image = image.convert("RGB")
        image = image.resize(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT),
            Image.Resampling.LANCZOS,
        )

        output = bytearray(expected_size)
        position = 0

        for red, green, blue in image.getdata():
            pixel = rgb888_to_rgb565(red, green, blue)
            output[position] = pixel >> 8
            output[position + 1] = pixel & 0xFF
            position += BYTES_PER_PIXEL

    output_path.write_bytes(output)

    actual_size = output_path.stat().st_size
    if actual_size != expected_size:
        raise RuntimeError(
            f"Expected {expected_size} bytes, wrote {actual_size} bytes"
        )

    print(f"Converted {source_path} to {output_path}")
    print(f"Size: {DISPLAY_WIDTH}x{DISPLAY_HEIGHT}, {actual_size} bytes")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PNG image to raw RGB565 for a 240x320 ST7789 display."
    )
    parser.add_argument("source", type=Path, help="Input PNG or other Pillow image")
    parser.add_argument("output", type=Path, help="Output .bin filename")
    arguments = parser.parse_args()

    convert_image(arguments.source, arguments.output)


if __name__ == "__main__":
    main()