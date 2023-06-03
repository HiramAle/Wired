class Dialog:
    def __init__(self, data: dict):
        self.text: list[str] = data.get("text", [])
        self.type: str = data.get("type", "")
        self.task: str = data.get("task", "")
        self.new_tasks: list[str] = data.get("new_tasks", [])
        self.add_item: list[str] = data.get("add_item", [])
        self.requirements: list[str] = data.get("requirements", [])
        self.consequences: list[str] = data.get("consequences", [])

    def __repr__(self):
        return f"Dialog ({self.type}, {' '.join(self.text)})"



