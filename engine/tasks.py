from engine.task_manager import TaskManager, Task


class Tasks:
    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def load_tasks(self, tasks: dict):
        self.tasks = {}
        for task_id, task_status in tasks.items():
            task = TaskManager.get_task(task_id)
            task.completed = task_status
            self.tasks[task_id] = task

    def add_task(self, task_id: str):
        if not TaskManager.exists(task_id):
            print(f"Task {task_id} doesn't exists")
            return
        self.tasks[task_id] = TaskManager.get_task(task_id)

    def tasks_of(self, task_type: str) -> list[Task]:
        return [task for task in self.tasks.values() if task.type == task_type]

    @property
    def tasks_dict(self) -> dict:
        return {task_id: task.completed for task_id, task in self.tasks.items()}

    def has(self, task_id: str) -> bool:
        if task_id in self.tasks.keys():
            return True
        return False

    def is_completed(self, task_id: str) -> bool:
        if not self.has(task_id):
            return False
        if not self.get(task_id).completed:
            return False
        return True

    def has_incomplete(self, task_id: str) -> bool:
        if not self.has(task_id):
            return False
        if self.get(task_id).completed:
            return False
        return True

    def get(self, task_id: str) -> Task | None:
        if not self.has(task_id):
            return None
        return self.tasks[task_id]

    @property
    def completed_tasks(self) -> list[Task]:
        return [task for task in self.tasks.values() if task.completed]

    @property
    def current_tasks(self) -> list[Task]:
        return [task for task in self.tasks.values() if not task.completed]
