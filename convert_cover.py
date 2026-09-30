"""Download Spotify cover art and store RGB565 binary files for the Pico."""

from io import BytesIO
from pathlib import Path
import pprint
import urllib.request
from typing import cast, Iterable

from PIL import Image

import APIcontrolla
ALBUMCOVERS_PATH = Path(__file__).with_name("ALBUMCOVERS.py")
COVERS_DIR = ALBUMCOVERS_PATH.with_name("covers")

def rgb888_to_rgb565(red, green, blue):
    return ((red & 0xF8) << 8) | ((green & 0xFC) << 3) | (blue >> 3)


def image_to_rgb565(image_data, size):
    """Convert image bytes to high-byte-first RGB565 display data."""
    with Image.open(BytesIO(image_data)) as image:
        image = image.convert("RGB").resize(
            (size, size),
            Image.Resampling.LANCZOS,
        )

        result = bytearray(size * size * 2)
        pixels = cast(Iterable[tuple[int, int, int]], image.getdata())
        for index, (red, green, blue) in enumerate(pixels):
            pixel = rgb888_to_rgb565(red, green, blue)
            result[index * 2] = pixel >> 8
            result[index * 2 + 1] = pixel & 0xFF

        return result


def download_image(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "spotify-controller-cover-converter"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # type: ignore[reportOptionalContextManager]
        return response.read()


def _get_cover_url(function, name):
    try:
        return function()
    except NameError as error:
        raise RuntimeError(
            f"APIcontrolla.{name}() returned an undefined variable. "
            "It should return its local url64/url300 value."
        ) from error


def load_albums():
    namespace = {}
    source = ALBUMCOVERS_PATH.read_text(encoding="utf-8")
    exec(compile(source, str(ALBUMCOVERS_PATH), "exec"), namespace)
    return namespace.get("albums", {})


def save_albums(albums):
    contents = "# holds RGB565 .bin files for 64x64 and 200x200 album covers\n"
    contents += "albums = "
    contents += pprint.pformat(albums, width=120, sort_dicts=False)
    contents += "\n"
    ALBUMCOVERS_PATH.write_text(contents, encoding="utf-8")


def save_cover(path, image_data, size):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_bytes(image_to_rgb565(image_data, size))
    temporary_path.replace(path)


def convert_current_album():
    album_id = APIcontrolla.getAlbumID()
    album_name = APIcontrolla.getAlbumName()
    url64 = _get_cover_url(APIcontrolla.getCoverURL64, "getCoverURL64")
    url300 = _get_cover_url(APIcontrolla.getCoverURL300, "getCoverURL300")

    file64 = COVERS_DIR / f"{album_id}-64.bin"
    file200 = COVERS_DIR / f"{album_id}-200.bin"
    save_cover(file64, download_image(url64), 64)
    save_cover(file200, download_image(url300), 200)

    albums = load_albums()
    album = albums.setdefault(album_id, {})
    album.pop("bytearray64", None)
    album.pop("bytearray200", None)
    album.update(
        {
            "name": album_name,
            "url64": url64,
            "url300": url300,
            "file64": file64.relative_to(ALBUMCOVERS_PATH.parent).as_posix(),
            "file200": file200.relative_to(ALBUMCOVERS_PATH.parent).as_posix(),
        }
    )
    save_albums(albums)
    print(f"Stored {album_name!r} ({album_id}) in {ALBUMCOVERS_PATH.name}")
    print("64x64 RGB565:", 64 * 64 * 2, "bytes")
    print("200x200 RGB565:", 200 * 200 * 2, "bytes")


if __name__ == "__main__":
    convert_current_album()

