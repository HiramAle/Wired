from typing import Any
from engine.loader import Loader


class Task:
    def __init__(self, task_id: str, data: dict):
        self.__data = data
        self.id = task_id
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.type: str = data.get("type")
        self.objective: str = data.get("objective")
        self.npcs: list[str] = data.get("npcs")
        self.consequence: str = data.get("consequence")
        self.completed = False

    def __repr__(self):
        return f"Task ({self.name}, {self.objective})"


class TaskManager:
    tasks: dict[str, Task] = {}

    @classmethod
    def load_tasks(cls):
        for id_task, task_data in Loader.load_json("data/world/tasks.json").items():
            cls.tasks[id_task] = Task(id_task, task_data)

    @classmethod
    def exists(cls, task_id: str) -> bool:
        if task_id in cls.tasks.keys():
            return True
        print(f"Task {task_id} doesn't exists.")
        return False

    @classmethod
    def get_task(cls, task_id: str) -> Task | None:
        if not cls.exists(task_id):
            return None
        return cls.tasks[task_id]


