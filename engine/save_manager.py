from engine.loader import Loader


class GameSave:
    def __init__(self, filename: str):
        save_data = Loader.load_json(filename)
        if not save_data:
            save_data = {"name": "",
                         "pronoun": "",
                         "time": 0,
                         "money": 0,
                         "cable": 0,
                         "connectors": 0,
                         "inventory": {}}
            Loader.save_json(filename, save_data)
        self.filename = filename
        self.name = save_data["name"]
        self.pronoun = save_data["pronoun"]
        self.time = save_data["time"]
        self.money = save_data["money"]
        self.cable = save_data["cable"]
        self.connectors = save_data["connectors"]
        self.inventory = save_data["inventory"]

    def __dict(self) -> dict:
        return {key: value for key, value in vars(self).items() if key != "filename"}

    def save(self):
        if Loader.save_json(self.filename, self.__dict()):
            print("File saved")
            return
        print("Can't save file")


class SaveManager:
    def __init__(self):
        self.__saves: list[GameSave] = []
        self.__slot = 0

    def load(self):
        for index in range(3):
            print(self.__slot)

    @property
    def active_save(self) -> GameSave | None:
        try:
            return self.__saves[self.__slot]
        except IndexError:
            print("Saves aren't loaded yet")
            return None

    @active_save.setter
    def active_save(self, slot: int):
        if slot >= len(self.__saves):
            print("Slot index must be between 0 and 2")
            return
        self.__slot = slot


instance = SaveManager()
