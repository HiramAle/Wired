from engine.inventory import Inventory
from engine.tasks import Tasks


class PlayerData:
    name = ""
    inventory = Inventory()
    tasks = Tasks()
    notify: callable = None
    tutorials = {}

    @classmethod
    def load(cls, money: int, inventory: dict, tasks: dict):
        cls.inventory.load_inventory(money, inventory)
        cls.tasks.load_tasks(tasks)

    @classmethod
    def add_task(cls, task_id: str):
        cls.tasks.add_task(task_id)
        if cls.notify:
            print("Adding notification")
            cls.notify(f"Tarea añadida:\n{cls.tasks.get(task_id).name}", 3)

    @classmethod
    def add_item(cls, item_id: str, quantity=1):
        cls.inventory.add_item(item_id, quantity)
        for task in [task for task in cls.tasks.current_tasks if task.type == "has"]:
            task_item, task_quantity = task.objective.split(" ")
            if not cls.inventory.has_enough(task_item, int(task_quantity)):
                continue
            cls.complete_task(task.id)

    @classmethod
    def complete_task(cls, task_id: str):
        if not cls.tasks.has(task_id):
            return
        task = cls.tasks.get(task_id)
        task.completed = True
        print(f"Task {task_id} completed")
        print(f"Next task {task.next_task}")
        if task.next_task != "":
            cls.add_task(task.next_task)
            print(f"Adding task {task.next_task}")

    @classmethod
    def remove_item(cls, item_id: str, quantity: int = 1):
        cls.inventory.remove_item(item_id, quantity)
