from engine.loader import Loader
from typing import Any


class Item:
    def __init__(self, data: dict):
        self.__data = data
        self.name = data.get("name")
        self.description = data.get("description")

    def set(self, key: str, value: Any) -> bool:
        if key not in self.__data:
            print(f"{self.name} doesn't have {key} attribute")
            return False
        self.__data[key] = value
        return True

    def get(self, key: str) -> Any:
        if key not in self.__data:
            print(f"{self.name} doesn't have {key} attribute")
            return None
        return self.__data[key]


class Inventory:
    __all_items: dict[str, Item] = {}
    items: dict[str, int] = {}
    money = 0

    @classmethod
    def load_inventory(cls, inventory: dict, money: int):
        cls.money = money
        for id_item, quantity in inventory.items():
            cls.items[id_item] = quantity

    @classmethod
    def load_items(cls):
        all_items = Loader.load_json("data/world/items.json")
        for id_item, item_data in all_items.items():
            cls.__all_items[id_item] = Item(item_data)

    @classmethod
    def add_item(cls, item_id: str, quantity: int = 1):
        if not cls.exists(item_id):
            print(f"Item {item_id} doesn't exists.")
            return
        if cls.has(item_id):
            cls.items[item_id] += quantity
        else:
            cls.items[item_id] = quantity

    @classmethod
    def remove_item(cls, item_id: str, quantity: int = 1):
        if not cls.has(item_id):
            print(f"Player doesn't have {item_id}")
            return
        cls.items[item_id] -= quantity
        if cls.items[item_id] <= 0 and item_id not in ["cable", "connector"]:
            cls.items.pop(item_id)

    @classmethod
    def has(cls, item_id: str) -> bool:
        return item_id in cls.items.keys()

    @classmethod
    def exists(cls, item_id: str) -> bool:
        return item_id in cls.__all_items.keys()

    @classmethod
    def has_enough(cls, item_id: str, quantity: int) -> bool:
        if not cls.has(item_id):
            return False
        return cls.items[item_id] >= quantity

    @classmethod
    def how_much(cls, item_id: str) -> int:
        if not cls.has(item_id):
            return 0
        return cls.items[item_id]

    @classmethod
    def print_inventory(cls):
        for item, quantity in cls.items.items():
            print(f"{cls.__all_items[item].name} ({quantity})")
