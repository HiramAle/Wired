import os

import pytmx
from src.utils.load import load_json
from src.constants.paths import *

cable_data = {}
tiled_map = None
character_creation_frames: dict[str, dict[str, int]] = {}
body_colors: dict[int, tuple] = {}
eyes_colors: dict[int, tuple] = {}
hairstyle_colors: dict[str, dict[int, tuple]] = {}
outfit_colors: dict[int, dict[int, tuple]] = {}
subnetting: dict[int, dict] = {}


def init():
    global cable_data, tiled_map, character_creation_frames
    global body_colors, eyes_colors, hairstyle_colors, outfit_colors
    global subnetting
    cable_data = load_json(DATA_CABLES)
    tiled_map = pytmx.load_pygame(TILED_HOUSE, pixelalpha=True)
    character_creation_frames = load_json(DATA_CHARACTER_CREATION_FRAMES)
    body_colors = {int(key): tuple(value) for key, value in load_json(BODY_COLORS).items()}
    eyes_colors = {int(key): tuple(value) for key, value in load_json(EYES_COLORS).items()}

    hairstyle_colors = convert_dictionary(load_json(HAIRSTYLE_COLORS))
    outfit_colors = convert_dictionary(load_json(OUTFIT_COLORS))

    subnetting = {int(file.split(".")[0]): load_json(f"{SUBNETTING_EXERCISES}/{file}") for file in
                  os.listdir(SUBNETTING_EXERCISES)}


def convert_dictionary(dictionary: dict):
    new_dictionary = {}
    for key, value in dictionary.items():
        if key.isnumeric():
            new_key = int(key)
        else:
            new_key = key
        new_value = {}
        for k, v in value.items():
            new_value[int(k)] = tuple(v)
        new_dictionary[new_key] = new_value
    return new_dictionary
