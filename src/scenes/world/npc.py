import random

import pygame
import src.utils.load as load
from engine.assets import Assets
from src.scenes.world.actor import Actor, Emote
from src.constants.paths import NPC_SPRITE_SHEETS, NPC_DATA
from engine.input import Input
from engine.dialog_manager import Dialog
from src.scenes.world.time_manager import TimeManager
from engine.playerdata import PlayerData


class Route:
    def __init__(self, name: str, nodes: list, zone: str, time: int):
        self.name = name
        self.nodes: list[tuple[float, float]] = nodes
        self.zone = zone
        self.time = time
        self._index = 0

    @property
    def finished(self) -> bool:
        return self._index >= len(self.nodes)

    @property
    def target(self) -> pygame.Vector2:
        return pygame.Vector2(self.nodes[self._index])

    def next(self):
        self._index += 1

    def reset(self):
        self._index = 0


class NPC(Actor):
    def __init__(self, name: str, player: Actor):
        path = f"{NPC_SPRITE_SHEETS}/{name}.png"
        super().__init__((0, 0), path, [])
        self.name = name
        self.data = load.load_json(f"{NPC_DATA}/{name}.json")
        self.dialogs: list[Dialog] = [Dialog(dialog_data) for dialog_data in self.data["dialogs"].values()]
        self.routes = []
        self.node_index = 0
        self.speed = 100
        self.active_route: Route | None = None
        self.current_zone = self.data["start_zone"]
        self.set_zone()
        self.talkable = False
        self.player = player

    def __repr__(self):
        return f"NPC({self.name}, {self.position})"

    def set_zone(self):
        requirement = self.data.get("requirement", "")
        if requirement == "":
            return
        if not PlayerData.tasks.is_completed(requirement):
            return
        schedule = self.data.get("schedule", {})
        if not schedule:
            return
        self.current_zone = schedule[str(TimeManager.current_day_of_week)]

    def get_dialogs(self, dialog_type: str) -> list[Dialog]:
        return [dialog for dialog in self.dialogs if dialog.type == dialog_type]

    def get_special_dialog(self) -> Dialog:
        from engine.playerdata import PlayerData
        special_dialogs = self.get_dialogs("special")
        print(f"Looking up for possible unique dialogs in {special_dialogs}")
        for dialog in special_dialogs:
            if dialog.other_requirement.startswith("has"):
                item_id = dialog.other_requirement.split(" ")[1]
                quantity = int(dialog.other_requirement.split(" ")[2])
                if PlayerData.inventory.has_enough(item_id, quantity):
                    give_item_id, give_quantity = dialog.add_item.split(" ")
                    PlayerData.add_item(give_item_id, int(give_quantity))
                    return dialog
            elif dialog.other_requirement == "poor":
                if PlayerData.inventory.money == 0:
                    PlayerData.add_item("money", 200)
                    return dialog

    def generic_dialog(self) -> Dialog:
        from engine.playerdata import PlayerData
        generic_dialogs = self.get_dialogs("generic")
        dialogs = []
        for dialog in generic_dialogs:
            if not dialog.requirement:
                dialogs.append(dialog)
                continue
            requirements_done = True
            for requirement, status in dialog.requirement.items():
                # Return the task from the player tasks, or None if the player doesn't have the task
                task = PlayerData.tasks.get(requirement)
                if not task:
                    requirements_done = False
                    break
                if status == 1:
                    if not task.completed:
                        requirements_done = False
                elif status == 0:
                    if task.completed:
                        requirements_done = False
            if requirements_done:
                dialogs.append(dialog)
        if not dialogs:
            dialog = Dialog({"text": ["Hola"], "type": "generic", "mission_requirement": {}})
        else:
            dialog = random.choice(dialogs)
        print(f"Selected dialog {dialog}")
        return dialog

    def task_complete_dialog(self, mission_id: str) -> Dialog:
        dialogs = [dialog for dialog in self.dialogs if dialog.type == "mission_complete"]
        print(self.name, dialogs)
        for dialog in dialogs:
            requirement_mission = list(dialog.requirement.keys())[0]
            print(f"Is {requirement_mission} = {mission_id}? {requirement_mission == mission_id}")
            if list(dialog.requirement.keys())[0] == mission_id:
                return dialog

    @property
    def player_distance(self) -> float:
        return (self.position - self.player.position).magnitude()

    def interact(self) -> bool:
        if self.player_distance <= 50 and Input.keyboard.keys["interact"]:
            return True

    def update(self):
        self.update_status()
        self.animate()
        self.move()
