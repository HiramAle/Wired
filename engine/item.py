from typing import Any


class Item:
    def __init__(self, item_id: str, data: dict):
        self.__data = data
        self.id = item_id
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
