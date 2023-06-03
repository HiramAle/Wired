from engine.inventory import Inventory
from engine.tasks import Tasks


class PlayerData:
    name = ""
    inventory = Inventory()
    tasks = Tasks()
    notify: callable = None
    tutorials = {}
    statuses = []
    pronoun = "elle"

    @classmethod
    def data_repr(cls):
        return f"Data ({cls.name}, {cls.inventory.items}, {cls.tasks.tasks}, {cls.tutorials})"

    @classmethod
    def load(cls, money: int, inventory: dict, tasks: dict):
        cls.inventory.load_inventory(money, inventory)
        cls.tasks.load_tasks(tasks)

    @classmethod
    def add_task(cls, task_id: str):
        cls.tasks.add_task(task_id)
        if cls.notify:
            print("Adding notification")
            cls.notify(f"Tarea añadida:\n{cls.tasks.get(task_id).title}", 3)

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
        if cls.notify:
            extra = ""
            if task.next_tasks:
                extra = "Nuevas tareas añadidas."
            cls.notify(f"Tarea {task.title} completada! {extra}", 3)
        for new_task in task.next_tasks:
            cls.add_task(new_task)

    @classmethod
    def remove_item(cls, item_id: str, quantity: int = 1):
        cls.inventory.remove_item(item_id, quantity)
