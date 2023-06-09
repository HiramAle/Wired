from __future__ import annotations
import enum
import math
import pygame
from engine.assets import Assets
from engine.time import Time
from engine.input import Input
from engine.objects.sprite import Sprite
from engine.ui.text import Text
from src.constants.colors import *
from random import randint
from engine.constants import Colors


class Subnet:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.id: str = data["id"]
        self.broadcast: str = data["broadcast"]
        self.firstUsable: str = data["first"]

    def __repr__(self):
        return f"{self.name}: {self.id}"


class SubnettingExercise:
    def __init__(self, zone_id: str, data: dict):
        self.zone_name = data.get("name")
        self.zone_id = zone_id
        self.buildings: list[Building] = []
        self.areas = data.get("areas")
        self.data: dict = data
        self.ip: str = self.data["ip"]
        self.ipClass: str = self.data["class"]
        self.defaultMask: str = self.data["default_mask"]
        self.subnetsNeeded: int = self.data["subnets_needed"]
        self.customMask: str = self.data["custom_mask"]
        self.subnets: list[Subnet] = [Subnet(name, data) for name, data in self.data["subnets"].items()]
        self.blanks = self.defaultMask.count("0")
        self.correctAnswers = self.customMask.split(".")[4 - self.blanks:]

    def subnet_answers(self, index: int) -> list:
        subnet = self.subnets[index]
        number = 4 - self.ip.split(".").count("0")
        id_answers = subnet.id.split(".")[number:]
        broadcast_answers = subnet.broadcast.split(".")[number:]
        return id_answers + broadcast_answers


class Building(Sprite):
    def __init__(self, position: tuple, building_type: str, *groups, **kwargs):
        super().__init__(position, Assets.images_subnetting["test_house"], *groups, **kwargs)
        self.building_type = building_type
        self.default_image = Assets.images_subnetting["test_house"]
        self.outline_image = Assets.images_subnetting["test_house_outline"]
        self.done_image = Assets.images_subnetting["test_house_outline_green"]
        self._selected = False
        self.subnet = Subnet("", {"id": "", "broadcast": "", "first": ""})
        self.done = False
        self.overlay = InfoOverlay(self)

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
            self.overlay.position = Input.mouse.x, Input.mouse.y - 25
            self.overlay.update()
        if self.subnet.name != "" and self.overlay.subnet_id.text == "":
            self.overlay.subnet_id.text = f"De {self.subnet.id} a\n{self.subnet.broadcast}"
        if self.done and self.image != self.done_image:
            self.image = self.done_image

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display, offset)
        if self.hovered and self.scale == 1:
            self.overlay.render(display)


class InfoOverlay(Sprite):
    def __init__(self, building: Building):
        super().__init__((0, 0), Assets.images_subnetting["house_ui"])
        self.clean_image = self.image.copy()
        self.building = building
        self.building_name = Text((self.rect.width / 2, 8), " ".join(self.building.building_type.splitlines()), 16,
                                  Colors.SPRITE)
        self.subnet_id = Text((8, 15), "", 16, Colors.SPRITE, centered=False)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        self.image = self.clean_image.copy()
        self.building_name.render(self.image)
        self.subnet_id.render(self.image)
        super().render(display)


class LabelStates(enum.Enum):
    FULL = 0
    STICK = 1


class ClassLabel(Sprite):
    def __init__(self, position: tuple, net_class: str, *groups, **kwargs):
        image = Assets.images_subnetting[f"class_{net_class}"]
        super().__init__(position, image, *groups, **kwargs)
        self.network_class = net_class
        self._state = LabelStates.STICK
        self.default_position = position

    def reposition(self):
        self.position = self.default_position
        self.state = LabelStates.STICK

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
            self.image = Assets.images_subnetting[f"class_{self.network_class}"]
        elif value == LabelStates.FULL:
            self.image = Assets.images_subnetting[f"class{self.network_class}_full"]
        self._state = value

    def update(self, *args, **kwargs):
        ...


class LabelHolder(Sprite):
    def __init__(self, position: tuple, *groups, **kwargs):
        image = Assets.images_subnetting["label_holder"]
        super().__init__(position, image, *groups, **kwargs)
        self.label: Label | None = None
        self.centered = False


class Label(Sprite):
    def __init__(self, position: tuple, value: int, static=False, *groups, **kwargs):
        image = Assets.images_subnetting["label_full"] if static else Assets.images_subnetting["label"]
        super().__init__(position, image, *groups, **kwargs)
        self.default_position = position
        self._value = value
        self._state = LabelStates.STICK
        self.text = Text(self.rect.center, str(value), 32, Colors.DARK, shadow=False)
        self.holder: LabelHolder = kwargs.get("holder", None)
        self.can_move = False if static else True
        self.shifting = False
        self.shift_position = (0, 0)

    def reposition(self):
        self.position = self.default_position
        self.state = LabelStates.STICK

    def shift(self):
        if not self.shifting:
            return

        if math.dist(self.shift_position, self.position) < 2:
            self.shifting = False
            return

        self.y -= (self.y - Input.mouse.y) / (0.01 / Time.dt)
        self.x -= (self.x - Input.mouse.x) / (0.01 / Time.dt)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
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
            self.image = Assets.images_subnetting["label"]
        elif value == LabelStates.FULL:
            self.image = Assets.images_subnetting["label_full"]
        self._state = value
