from engine.inventory import Inventory
from engine.tasks import Tasks


class PlayerData:
    name = ""
    inventory = Inventory()
    tasks = Tasks()

    @classmethod
    def load(cls, money: int, inventory: dict, tasks: dict):
        cls.inventory.load_inventory(money, inventory)
        cls.tasks.load_tasks(tasks)

    @classmethod
    def add_item(cls, item_id: str, quantity=1):
        cls.inventory.add_item(item_id, quantity)
        for task in [task for task in cls.tasks.current_tasks if task.type == "has"]:
            task_item, task_quantity = task.objective.split(" ")
            if not cls.inventory.has_enough(task_item, int(task_quantity)):
                continue
            task.completed = True

    @classmethod
    def remove_item(cls, item_id: str, quantity: int = 1):
        cls.inventory.remove_item(item_id, quantity)
