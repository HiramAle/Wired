class Dialog:
    def __init__(self, data: dict):
        self.text: list[str] = data.get("text")
        self.type: str = data.get("type")
        self.requirement: dict[str, int] = data.get("mission_requirement")
        self.add_mission: str = data.get("add_mission", "")
        self.add_item: str = data.get("add_item", "")
        self.other_requirement: str = data.get("requirement", "")

    def __repr__(self):
        return f"Dialog ({self.type}, {self.requirement})"
