import os
from hashlib import sha1
from pathlib import Path

from PIL import Image


BG_COLOR = (255, 255, 0)
TEMPLATES_PATH = Path(__file__).parent / "templates"


bodies = {}
eyes = {}
head = {}
mouse = {}
shirt = {}


def make_avatar(username: str, dest_path: str):
    _prepare_templates()

    img = Image.new("RGB", (16, 16))

    body_num, eyes_num, head_num, mouse_num, shirt_num = \
        _get_template_nums_from_username(username)

    _set_pixels(img, bodies[body_num])
    _set_pixels(img, eyes[eyes_num])
    _set_pixels(img, head[head_num])
    _set_pixels(img, mouse[mouse_num])
    _set_pixels(img, shirt[shirt_num])

    img.save(os.path.join(dest_path, "default.png"))


def _make_collection(coll_folder: str, coll: dict):
    for subc in os.listdir(TEMPLATES_PATH / coll_folder):
        img = Image.open(TEMPLATES_PATH / coll_folder / subc)
        key = subc.split("_")[1].split(".")[0]
        coll[key] = []
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pixel = img.getpixel((x, y))
                if pixel != BG_COLOR:
                    coll[key].append((pixel, (x, y)))


def _set_pixels(image: Image.Image, colors_pos: list):
    for color, pos in colors_pos:
        image.putpixel(pos, color)


def _prepare_templates():
    for col, dict_ in zip(
        ["body", "eyes", "head", "mouse", "shirt"],
        [bodies, eyes, head, mouse, shirt]
    ):
        _make_collection(col, dict_)


def _get_template_nums_from_username(username: str):
    from random import randint

    username_hash = sha1(username.encode()).hexdigest()

    valid_hex_from_hash = "".join(char for char in username_hash if char in "0123456")
    hash_len = len(valid_hex_from_hash)
    if hash_len < 5:
        valid_hex_from_hash = (
            valid_hex_from_hash +
            "".join(
                str(randint(0, 6)) for _ in range(5-hash_len)
            )
        )

    return tuple(valid_hex_from_hash[:5])
