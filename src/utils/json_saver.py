import json
from src.constants.paths import SAVES_FOLDER


class GameSave:
    def __init__(self, filename: str):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"name": "",
                    "pronoun": "",
                    "time": 0,
                    "money": 0,
                    "cable": 0,
                    "connectors": 0,
                    "inventory": {}}
            with open(filename, "w") as file:
                json.dump(data, file, indent=2)

        self.filename = filename
        self.name = data["name"]
        self.pronoun = data["pronoun"]
        self.time = data["time"]
        self.money = data["money"]
        self.cable = data["cable"]
        self.connectors = data["connectors"]
        self.inventory = data["inventory"]

    def to_dict(self) -> dict:
        return {"name": self.name, "pronoun": self.pronoun, "time": self.time, "money": self.money, "cable": self.cable,
                "connectors": self.connectors, "inventory": self.inventory}

    def save(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(self.to_dict(), file, indent=2)
            print("File saved")
        except FileNotFoundError:
            print("Unable to save file.")


class SaveManager:
    def __init__(self):
        self.saves: list[GameSave] = []
        self.index = 0

        for index in range(3):
            self.saves.append(GameSave(f"{SAVES_FOLDER}/save_{index}/save.json"))

    @property
    def game_save(self) -> GameSave:
        return self.saves[self.index]

    @game_save.setter
    def game_save(self, value: int):
        self.index = value


instance = SaveManager()
