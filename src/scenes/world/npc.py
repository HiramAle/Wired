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
    def __init__(self, name: str, player: Actor = None):
        path = f"{NPC_SPRITE_SHEETS}/{name}.png"
        super().__init__((0, 0), path, [])
        self.name = name
        self.data = load.load_json(f"{NPC_DATA}/{name}.json")
        self.dialogs: list[Dialog] = [Dialog(dialog_data) for dialog_data in self.data["dialogues"]]
        self.routes = []
        self.node_index = 0
        self.speed = 100
        self.active_route: Route | None = None
        self.current_zone = self.data["default_zone"]
        self.set_zone()
        self.talkable = False
        self.player = player

    def __repr__(self):
        return f"NPC({self.name}, {self.position})"

    def set_direction(self):
        direction = self.player.position - self.position
        direction.normalize_ip()
        if direction.y > 0.5:
            self.direction = "down"
        elif direction.y < -0.5:
            self.direction = "up"
        elif direction.x > 0.5:
            self.direction = "right"
        else:
            self.direction = "left"

    def set_zone(self):
        if not PlayerData.tasks.is_completed("meet_chencho"):
            return
        schedule = self.data.get("schedule")
        self.current_zone = schedule[str(TimeManager.current_day_of_week)]

    def get_dialogs(self, dialog_type: str) -> list[Dialog]:
        return [dialog for dialog in self.dialogs if dialog.type == dialog_type]

    def check_dialog_requirements(self, requirements: list[str]) -> bool:
        for requirement in requirements:
            requirement_type, object_id, object_param = requirement.split(" ")
            if requirement_type == "task" and object_param == "1":
                if not PlayerData.tasks.is_completed(object_id):
                    return False
            if requirement_type == "task" and object_param == "0":
                if PlayerData.tasks.is_completed(object_id):
                    return False
            if requirement_type == "has_exact":
                if PlayerData.inventory.how_much(object_id) != object_param:
                    return False
            if requirement_type == "has_enough":
                if not PlayerData.inventory.has_enough(object_id, object_param):
                    return False
            if requirement_type == "consequence":
                if object_id not in PlayerData.statuses:
                    return False
            if requirement_type == "npc_is_in":
                if self.current_zone != object_id:
                    return False

        return True

    def task_complete_dialog(self) -> Dialog | None:
        print(PlayerData.tasks.current_tasks)
        for task in PlayerData.tasks.current_tasks:
            print(f"Checking {task.id}, {self.name.lower()} = {task.objective}?")
            if self.name.lower() == task.objective:
                # Find task where the objective is talk to the NPC
                dg = None
                for dialog in self.get_dialogs("task_complete"):
                    if dialog.task == task.id:
                        dg = dialog
                        break
                # If it finds it check the requirements
                if not dg:
                    continue
                if not self.check_dialog_requirements(dg.requirements):
                    continue
                for command in dg.add_item:
                    item_id, quantity = command.split(" ")
                    PlayerData.add_item(item_id, int(quantity))
                # Complete task
                PlayerData.complete_task(task.id)
                return dg
        return None

    def get_new_task_dialog(self) -> Dialog | None:
        for dialog in self.get_dialogs("new_task"):
            if not self.check_dialog_requirements(dialog.requirements):
                continue
            for new_task_id in dialog.new_tasks:
                if new_task_id in PlayerData.tasks.tasks:
                    continue
                PlayerData.add_task(new_task_id)
                return dialog
        return None

    def get_add_item_dialog(self) -> Dialog | None:
        for dialog in self.get_dialogs("add_item"):
            if not self.check_dialog_requirements(dialog.requirements):
                continue
            for item_command in dialog.add_item:
                item_id, quantity = item_command.split(" ")
                PlayerData.add_item(item_id, quantity)
            return dialog
        return None

    def get_generic_dialog(self) -> Dialog:
        generic_dialogs = self.get_dialogs("generic")
        possible_dialogs = []
        for dialog in generic_dialogs:
            # If generic dialog doesn't have any requirements, is added to the possible dialogs
            if not dialog.requirements:
                possible_dialogs.append(dialog)
                continue
            if not self.check_dialog_requirements(dialog.requirements):
                continue
            possible_dialogs.append(dialog)

        if not possible_dialogs:
            dialog = Dialog({"text": ["Hola"]})
        else:
            dialog = random.choice(possible_dialogs)
        if dialog.consequences:
            for consequence in dialog.consequences:
                req_type, add_consequence = consequence.split(" ")
                PlayerData.statuses.append(add_consequence)
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
