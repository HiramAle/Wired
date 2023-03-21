from __future__ import annotations
import pygame
from enum import Enum
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.game_object.game_object import GameObject
import src.scene.scene_manager as scene_manager


class Transitions(Enum):
    CIRCULAR = 0


class Scene:
    def __init__(self, name: str):
        self.name = name
        self.display = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.transitionPosition = self.center
        self._objects: list[GameObject] = []

    @property
    def center_x(self):
        return self.display.get_size()[0] / 2

    @property
    def center_y(self):
        return self.display.get_size()[1] / 2

    @property
    def center(self) -> tuple:
        return self.center_x, self.center_y

    def add(self, new_object: GameObject):
        self._objects.append(new_object)

    def update_objects(self):
        for game_object in self._objects:
            if game_object.active:
                game_object.update()

    def update(self) -> None:
        ...

    def render(self) -> None:
        ...
