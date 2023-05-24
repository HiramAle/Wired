from typing import Any

from engine.loader import Loader


class Task:
    def __init__(self, data: dict):
        self.__data = data
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.type: str = data.get("type")
        self.objective: str = data.get("objective")
        self.consequence: str = data.get("consequence")
        self.completed = False

    def __repr__(self):
        return f"Task ({self.name}, {self.objective})"

    def has_objective(self, objective: str) -> bool:
        if objective in self.objective:
            return True
        print(f"{self.name} doesn't have objective {objective}")
        return False

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


class TaskManager:
    __tasks: dict[int, Task] = {}
    tasks: dict[int, Task] = {}

    @classmethod
    def get_current_tasks(cls) -> list[Task]:
        current_tasks = []
        for task_id, task in cls.tasks.items():
            if task.completed:
                continue
            current_tasks.append(task)
        return current_tasks

    @classmethod
    def load_tasks(cls):
        all_tasks = Loader.load_json("data/world/tasks.json")
        for id_task, task_data in all_tasks.items():
            cls.__tasks[int(id_task)] = Task(task_data)
        print("Loaded tasks: ", cls.__tasks)

    @classmethod
    def load_player_tasks(cls, tasks: dict):
        for id_task in tasks:
            cls.tasks[int(id_task)] = cls.__tasks[int(id_task)]
            cls.tasks[int(id_task)].completed = tasks[id_task]
        print("Player tasks: ", cls.tasks)

    @classmethod
    def get_tasks_from_type(cls, task_type: str) -> list[int]:
        filtered_tasks = []
        for task_id in cls.tasks:
            task = cls.get_task(task_id)
            if task.type != task_type:
                continue
            filtered_tasks.append(task_id)
        print(f"filtered tasks {filtered_tasks} of {task_type} type")
        return filtered_tasks

    @classmethod
    def get_task(cls, task_id) -> Task | None:
        if not cls.has(task_id):
            return None
        return cls.tasks[task_id]

    @classmethod
    def exists(cls, task_id: int) -> bool:
        print(f"{task_id} in {cls.__tasks.keys()}?")
        if task_id in cls.__tasks.keys():
            return True
        print(f"Task {task_id} doesn't exists")
        return False

    @classmethod
    def has(cls, task_id: int) -> bool:
        print(f"{task_id} in {cls.tasks.keys()}?")
        if task_id in cls.tasks.keys():
            return True
        print(f"Player doesn't have task {task_id}")
        return False

    @classmethod
    def create_task(cls, task_id: int, data: dict):
        if cls.exists(task_id):
            print(f"Task {task_id} already exists")
            return
        print(f"Creating new task")
        cls.__tasks[task_id] = Task(data)

    @classmethod
    def add_task(cls, task_id: int):
        if not cls.exists(task_id):
            return
        if cls.has(task_id):
            return
        print(f"Adding task {cls.__tasks[task_id]}")
        new_task = cls.__tasks[task_id]
        cls.tasks[task_id] = new_task
        from engine.save_manager import instance as save_manager
        save_manager.active_save.tasks[task_id] = False
        save_manager.active_save.status[new_task.consequence] = False

    @classmethod
    def complete_task(cls, task_id: int):
        if not cls.has(task_id):
            return

        if cls.tasks[task_id].completed:
            return
        print(f"Task {cls.tasks[task_id].name} completed")
        from engine.save_manager import instance as save_manager
        cls.tasks[task_id].completed = True
        save_manager.active_save.tasks[task_id] = True
        save_manager.active_save.status[cls.tasks[task_id].consequence] = True
