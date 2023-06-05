import os

import pygame.time

from engine.loader import Loader
from engine.constants import Paths
from engine.playerdata import PlayerData


class GameSave:
    def __init__(self, folder_path: str):
        self.filename = f"{folder_path}/save.json"
        self.sprite_sheet = f"{folder_path}/sprite_sheet.png"
        self.portrait = f"{folder_path}/portrait.png"
        save_data = Loader.load_json(f"{folder_path}/save.json")
        if not save_data:
            save_data = {"name": "",
                         "pronoun": "",
                         "week_day": 0,
                         "time": 0,
                         "money": 200,
                         "inventory": {
                         },
                         "tutorials": {
                             "cables": False,
                             "subnetting": False,
                             "routing": False
                         },
                         "tasks": {
                             "meet_kat": False
                         },
                         "status": {
                         }
                         }
            Loader.save_json(self.filename, save_data)
        self.name = save_data["name"]
        self.week_day = save_data["week_day"]
        self.pronoun = save_data["pronoun"]
        self.time = save_data["time"]
        self.money = save_data["money"]
        self.inventory = save_data["inventory"]
        self.tutorials = save_data["tutorials"]
        self.tasks = save_data["tasks"]
        self.status = save_data["status"]

    def erase(self):
        save_data = {"name": "",
                     "pronoun": "",
                     "week_day": 0,
                     "time": 0,
                     "money": 200,
                     "inventory": {
                     },
                     "tutorials": {
                         "cables": False,
                         "subnetting": False,
                         "routing": False
                     },
                     "tasks": {
                         "meet_kat": False
                     },
                     "status": {
                     }
                     }
        self.name = save_data["name"]
        self.week_day = save_data["week_day"]
        self.pronoun = save_data["pronoun"]
        self.time = save_data["time"]
        self.money = save_data["money"]
        self.inventory = save_data["inventory"]
        self.tutorials = save_data["tutorials"]
        self.tasks = save_data["tasks"]
        self.status = save_data["status"]
        Loader.save_json(self.filename, save_data)

    def to_dict(self) -> dict:
        return {key: value for key, value in vars(self).items() if key not in ["filename"]}


class SaveManager:
    def __init__(self):
        self.saves: list[GameSave] = []
        self.__slot = 0

    def load(self):
        for index, folder in enumerate(os.listdir(Paths.USER_SAVES_FOLDER)):
            self.saves.append(GameSave(f"{Paths.USER_SAVES_FOLDER}/{folder}"))

    def erase_save(self, save_index: int):
        self.saves[save_index].erase()

    def save(self):
        self.active_save.money = PlayerData.inventory.money
        self.active_save.inventory = PlayerData.inventory.items
        self.active_save.tasks = PlayerData.tasks.tasks_dict
        self.active_save.tutorials = PlayerData.tutorials

        if Loader.save_json(self.active_save.filename, self.active_save.to_dict()):
            print("File saved")
            return
        print("Can't save file")

    def delete(self, save_index: int):
        save = self.saves[save_index]
        if save.name != "":
            save.erase()

    @property
    def active_save(self) -> GameSave | None:
        try:
            return self.saves[self.__slot]
        except IndexError:
            print("Saves aren't loaded yet")
            return None

    @active_save.setter
    def active_save(self, slot: int):
        if slot >= len(self.saves):
            print("Slot index must be between 0 and 2")
            return
        self.__slot = slot
        self.reload_data()

    def reload_data(self):
        PlayerData.load(self.active_save.money, self.active_save.inventory, self.active_save.tasks)
        PlayerData.name = self.active_save.name
        PlayerData.tutorials = self.active_save.tutorials
        PlayerData.pronoun = self.active_save.pronoun


instance = SaveManager()
