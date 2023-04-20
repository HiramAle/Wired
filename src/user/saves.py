from os import listdir, mkdir
from src.constants.paths import SAVES_FOLDER
from src.utils.load import load_json, write_json

saves: list[dict] = []


def init() -> None:
    try:
        load_saves()
    except FileNotFoundError:
        for index in range(3):
            save_data = {"name": ""}
            write_json(f"{SAVES_FOLDER}/save_{index}/save.json", save_data)
        load_saves()


def load_saves():
    global saves
    for folder in listdir(SAVES_FOLDER):
        saves.append(load_json(f"{SAVES_FOLDER}/{folder}/save.json"))


def load_save_data(save_index: int) -> dict:
    global saves
    return saves[save_index]


def write_save_data(save_index: int, data: dict):
    global saves
    save_data = load_save_data(save_index)

    for key, value in data.items():
        save_data[key] = value
    write_json(f"{SAVES_FOLDER}/save_{save_index}/save.json", save_data)
    saves = []
    load_saves()
