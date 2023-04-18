import enum
import math

import pygame
import src.engine.assets as assets
import src.engine.time as game_time
import src.engine.input as game_input
import src.engine.data as game_data
from src.game_object.sprite import Sprite
from src.gui.text import GUIText
from src.constants.colors import *
from random import choice, randint


class Subnet:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.id: str = data["id"]
        self.broadcast: str = data["broadcast"]
        self.firstUsable: str = data["first"]

    def __repr__(self):
        return f"{self.name}: {self.id}"


class CustomMaskProblem:
    def __init__(self, zone: str, exercise=randint(1, 10)):
        self.zone = zone
        self.buildings: list[Building] = []
        self.data: dict = game_data.subnetting.get(exercise)
        self.ip: str = self.data["ip"]
        self.ipClass: str = self.data["class"]
        self.defaultMask: str = self.data["default_mask"]
        self.subnetsNeeded: int = self.data["subnets_needed"]
        self.customMask: str = self.data["custom_mask"]
        self.subnets: list[Subnet] = [Subnet(name, data) for name, data in self.data["subnets"].items()]
        self.blanks = self.defaultMask.count("0")
        self.correctAnswers = self.customMask.split(".")[4 - self.blanks:]
        print(self.customMask, self.blanks, self.correctAnswers)

    def subnet_answers(self, index: int) -> list:
        subnet = self.subnets[index]
        number = 4 - self.ip.split(".").count("0")
        id_answers = subnet.id.split(".")[number:]
        broadcast_answers = subnet.broadcast.split(".")[number:]
        return id_answers + broadcast_answers


class Building(Sprite):
    def __init__(self, position: tuple, building_type: str, *groups, **kwargs):
        super().__init__("building", position, assets.images_subnetting["test_house"], *groups, **kwargs)
        self.building_type = building_type
        self.default_image = assets.images_subnetting["test_house"]
        self.outline_image = assets.images_subnetting["test_house_outline"]
        self._selected = False
        self.name = GUIText(self.building_type, (self.rect.centerx + 7.5, self.rect.bottom - 5), 16)
        self.subnet_id = GUIText("", (self.rect.centerx + 7.5, self.rect.top + 5), 16)
        self.subnet = Subnet("", {"id": "", "broadcast": "", "first": ""})

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        if value == self._selected:
            return

        self.image = self.outline_image if value else self.default_image
        self._selected = value

    def update(self, *args, **kwargs):
        if self.hovered and self.scale == 1:
            self.name.position = game_input.mouse.x + 20, game_input.mouse.y - 20

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display, offset)
        if self.hovered and self.scale == 1:
            self.name.render(display)
        if self.subnet.name != "":
            self.subnet_id.text = self.subnet.id + "\n" + self.subnet.broadcast
            self.subnet_id.render(display)


class LabelStates(enum.Enum):
    FULL = 0
    STICK = 1


class ClassLabel(Sprite):
    def __init__(self, position: tuple, net_class: str, *groups, **kwargs):
        image = assets.images_subnetting[f"class_{net_class}"]
        super().__init__("class_label", position, image, *groups, **kwargs)
        self.network_class = net_class
        self._state = LabelStates.STICK

    def __repr__(self):
        return self.network_class

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: LabelStates):
        if value == self._state:
            return
        if value == LabelStates.STICK:
            self.image = assets.images_subnetting[f"class_{self.network_class}"]
        elif value == LabelStates.FULL:
            self.image = assets.images_subnetting[f"class{self.network_class}_full"]
        self._state = value

    def update(self, *args, **kwargs):
        ...


class LabelHolder(Sprite):
    def __init__(self, position: tuple, *groups, **kwargs):
        image = assets.images_subnetting["label_holder"]
        super().__init__("label_holder", position, image, *groups, **kwargs)
        self.label: Label | None = None
        self.centered = False


class Label(Sprite):
    def __init__(self, position: tuple, value: int, static=False, *groups, **kwargs):
        image = assets.images_subnetting["label_full"] if static else assets.images_subnetting["label"]
        super().__init__("label", position, image, *groups, **kwargs)
        self.default_position = position
        self._value = value
        self._state = LabelStates.STICK
        self.text = GUIText(str(value), self.rect.center, 32, font="monogram", shadow=False, color=DARK_BLACK_MOTION)
        self.holder: LabelHolder = kwargs.get("holder", None)
        self.can_move = False if static else True
        self.shifting = False
        self.shift_position = (0, 0)

    def shift(self):
        if not self.shifting:
            return

        if math.dist(self.shift_position, self.position) < 2:
            self.shifting = False
            return

        self.y -= (self.y - game_input.mouse.y) / (0.01 / game_time.dt)
        self.x -= (self.x - game_input.mouse.x) / (0.01 / game_time.dt)

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display, offset)
        self.text.render(display)

    def update(self, *args, **kwargs):
        self.text.position = self.rect.center
        if self.holder:
            self.position = self.holder.rect.center

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.text.text = str(value)
        self._value = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: LabelStates):
        if value == self._state:
            return
        if value == LabelStates.STICK:
            self.image = assets.images_subnetting["label"]
        elif value == LabelStates.FULL:
            self.image = assets.images_subnetting["label_full"]
        self._state = value
