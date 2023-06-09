from typing import Any

from engine.loader import Loader


class TaskManager:
    __tasks: dict[str, Task] = {}
    tasks: dict[str, Task] = {}

    @classmethod
    def get_current_tasks(cls) -> list[Task]:
        current_tasks = []
        for task_id, task in cls.tasks.items():
            if task.is_completed:
                continue
            current_tasks.append(task)
        return current_tasks

    @classmethod
    def load_tasks(cls):
        all_tasks = Loader.load_json("data/world/tasks.json")
        for id_task, task_data in all_tasks.items():
            cls.__tasks[id_task] = Task(task_data)
        print("Loaded tasks: ", cls.__tasks)

    @classmethod
    def load_player_tasks(cls, tasks: dict):
        for id_task in tasks:
            cls.tasks[id_task] = cls.__tasks[id_task]
            cls.tasks[id_task].is_completed = tasks[id_task]
        print("Player tasks: ", cls.tasks)

    @classmethod
    def get_tasks_from_type(cls, task_type: str) -> list[str]:
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
        if not cls.exists(task_id):
            return None
        return cls.__tasks[task_id]

    @classmethod
    def exists(cls, task_id: str) -> bool:
        print(f"{task_id} in {cls.__tasks.keys()}?")
        if task_id in cls.__tasks.keys():
            return True
        print(f"Task {task_id} doesn't exists")
        return False

    @classmethod
    def has(cls, task_id: str) -> bool:
        print(f"{task_id} in {cls.tasks.keys()}?")
        if task_id in cls.tasks.keys():
            return True
        print(f"Player doesn't have task {task_id}")
        return False

    @classmethod
    def create_task(cls, task_id: str, data: dict):
        if cls.exists(task_id):
            print(f"Task {task_id} already exists")
            return
        print(f"Creating new task")
        cls.__tasks[task_id] = Task(data)

    @classmethod
    def add_task(cls, task_id: str):
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
    def complete_task(cls, task_id: str):
        if not cls.has(task_id):
            return

        if cls.tasks[task_id].is_completed:
            return
        print(f"Task {cls.tasks[task_id].name} completed")
        from engine.save_manager import instance as save_manager
        cls.tasks[task_id].is_completed = True
        save_manager.active_save.tasks[task_id] = True
        save_manager.active_save.status[cls.tasks[task_id].consequence] = True
