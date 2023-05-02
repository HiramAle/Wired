import os
import threading

import pytmx
import src.utils.load as load
from src.constants.paths import *

cable_data = {}
maps = {}
character_creation_frames: dict[str, dict[str, int]] = {}
body_colors: dict[int, tuple] = {}
eyes_colors: dict[int, tuple] = {}
hairstyle_colors: dict[str, dict[int, tuple]] = {}
outfit_colors: dict[int, dict[int, tuple]] = {}
subnetting: dict[int, dict] = {}
active_save: int = 0


def init():
    global cable_data, players_house, character_creation_frames
    global body_colors, eyes_colors, hairstyle_colors, outfit_colors
    global subnetting, village
    cable_data = load.load_json(DATA_CABLES)
    character_creation_frames = load.load_json(DATA_CHARACTER_CREATION_FRAMES)
    body_colors = {int(key): tuple(value) for key, value in load.load_json(BODY_COLORS).items()}
    eyes_colors = {int(key): tuple(value) for key, value in load.load_json(EYES_COLORS).items()}

    hairstyle_colors = convert_dictionary(load.load_json(HAIRSTYLE_COLORS))
    outfit_colors = convert_dictionary(load.load_json(OUTFIT_COLORS))

    subnetting = {int(file.split(".")[0]): load.load_json(f"{SUBNETTING_EXERCISES}/{file}") for file in
                  os.listdir(SUBNETTING_EXERCISES)}


def load_map(event: threading.Event, map_name: str):
    global maps
    maps[map_name] = pytmx.load_pygame(MAPS[map_name], pixelalpha=True)
    event.clear()
    return maps[map_name]


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
