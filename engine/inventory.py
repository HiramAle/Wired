import random

from engine.loader import Loader
from engine.item import Item
from engine.item_manager import ItemManager


class Inventory:
    def __init__(self):
        self.money = 0
        self.items: dict[str, int] = {}

    def load_inventory(self, money: int, inventory: dict):
        self.items = {}
        self.money = money
        for id_item, quantity in inventory.items():
            self.items[id_item] = quantity

    def add_item(self, item_id: str, quantity: int = 1):
        if item_id == "money":
            self.money += quantity
            return
        if not ItemManager.exists(item_id):
            print(f"Item {item_id} doesn't exists.")
            return
        if self.has(item_id):
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id: str, quantity: int = 1):
        if not self.has(item_id):
            print(f"Player doesn't have {item_id}")
            return
        print(f"Player has {self.items[item_id]}")
        print(f"Removing {quantity}")
        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            self.items[item_id] = 0
        print(f"Player have {self.items[item_id]}")

    def has(self, item_id: str) -> bool:
        for item in self.items.keys():
            if item.startswith(item_id):
                return True
        return False

    def has_enough(self, item_id: str, quantity: int) -> bool:
        if item_id == "money":
            if self.money >= quantity:
                return True
            else:
                return False
        if not self.has(item_id):
            return False
        counter = 0
        for item, item_quantity in self.items.items():
            if not item.startswith(item_id):
                continue
            counter += item_quantity
        return counter >= quantity

    def how_much(self, item_id: str) -> int:
        if item_id == "money":
            return self.money
        if not self.has(item_id):
            return 0
        counter = 0
        for item, item_quantity in self.items.items():
            if not item.startswith(item_id):
                continue
            counter += item_quantity
        return counter

    def how_many(self, item_id: str) -> int:
        if item_id == "money":
            return self.money
        if not self.has(item_id):
            return 0
        return self.items[item_id]

    def remove_cable(self, cable_type: str, quantity: int) -> list[int]:
        print(f"Removing {quantity} of {cable_type}")
        cables = [cable for cable in self.items.keys() if cable.startswith(cable_type)]
        print(f"Player has {len(cables)} of {cable_type}")
        if len(cables) >= quantity:
            random.shuffle(cables)
            for cable in cables:
                self.remove_item(cable)
        return [int(cable[-1]) for cable in cables]
