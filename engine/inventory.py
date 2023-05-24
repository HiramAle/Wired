from engine.loader import Loader
from engine.item import Item
from engine.item_manager import ItemManager


class Inventory:
    items: dict[str, int] = {}
    money = 0

    @classmethod
    def load_inventory(cls, inventory: dict, money: int):
        cls.money = money
        for id_item, quantity in inventory.items():
            cls.items[id_item] = quantity
        print("loaded inventory as ", cls.items)

    @classmethod
    def add_item(cls, item_id: str, quantity: int = 1):
        if not ItemManager.exists(item_id):
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
    def has_enough(cls, item_id: str, quantity: int) -> bool:
        if not cls.has(item_id):
            return False
        return cls.items[item_id] >= quantity

    @classmethod
    def how_much(cls, item_id: str) -> int:
        if not cls.has(item_id):
            return 0
        return cls.items[item_id]
