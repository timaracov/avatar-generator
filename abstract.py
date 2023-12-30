import os

from hashlib import sha1

from PIL.Image import new



COLOR = "#ffff00"

RGB = tuple[int, int, int]


def make_image_from_username(username: str, destination: str, size: tuple[int, int] = (32, 32)):
    _generate_image(_hash_data(username), destination, size)


def _hash_data(data: str):
    return sha1(data.encode()).hexdigest()


def _get_colors_from_hash(hash: str) -> tuple[RGB, RGB]:
    hex_color = hash[:3] + hash[-3:]
    bg_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    fg_color = tuple(255-val for val in bg_color)
    return bg_color, fg_color


def _generate_image(
    username_hash: str,
    destination: str,
    size: tuple[int, int] = (64, 64),
):
    avatar = new("RGB", size)
    
    bg, fg = _get_colors_from_hash(username_hash)

    half = size[0]//2*size[1]
    if len(username_hash) < half:
        outline_hash = username_hash*half
    else:
        outline_hash = username_hash

    for x in range(size[0]):
        for y in range(size[1]):
            avatar.putpixel((x, y), value=bg)

    for x in range(size[0]//2):
        for y in range(size[1]):
            value = int(outline_hash[x*y], 16)
            if (x+y) % (value+1) in [0, 1, 2, 3]:
                avatar.putpixel((x, y), value=fg)
                avatar.putpixel((size[0]-x-1, y), value=fg)

    avatar.save("./avatar.jpg")
    avatar.save(os.path.join(destination, "abstract.png"))

