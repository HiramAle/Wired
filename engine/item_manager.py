from engine.loader import Loader
from engine.item import Item


class ItemManager:
    all_items: dict[str, Item] = {}

    @classmethod
    def load_items(cls):
        all_items = Loader.load_json("data/world/items.json")
        for id_item, item_data in all_items.items():
            cls.all_items[id_item] = Item(id_item, item_data)

    @classmethod
    def exists(cls, item_id: str) -> bool:
        return item_id in cls.all_items.keys()

    @classmethod
    def get_item_by_id(cls, item_id: str) -> Item | None:
        if not cls.exists(item_id):
            return None
        return cls.all_items[item_id]
