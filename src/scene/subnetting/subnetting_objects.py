import enum
import pygame
import src.engine.assets as assets
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
        self.data: dict = game_data.subnetting.get(exercise)
        self.ip: str = self.data["ip"]
        self.ipClass: str = self.data["class"]
        self.defaultMask: str = self.data["default_mask"]
        self.subnetsNeeded: int = self.data["subnets_needed"]
        self.customMask: str = self.data["custom_mask"]
        self.subnets: list[Subnet] = [Subnet(name, data) for name, data in self.data["subnets"].items()]
        self.blanks = self.defaultMask.count("0")
        self.correctAnswers = self.customMask.split(".")[4 - self.blanks:]
        self.house_positions: list[tuple] = []
        print(self.customMask, self.blanks, self.correctAnswers)


class Building(Sprite):
    def __init__(self, position: tuple, building_type: str, *groups, **kwargs):
        super().__init__("building", position, assets.images_subnetting["test_house"], *groups, **kwargs)
        self.building_type = building_type
        self.default_image = assets.images_subnetting["test_house"]
        self.outline_image = assets.images_subnetting["test_house_outline"]
        self._selected = False

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        if value == self._selected:
            return

        self.image = self.outline_image if value else self.default_image
        self._selected = value


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
