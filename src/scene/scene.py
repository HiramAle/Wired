from __future__ import annotations
import pygame
from enum import Enum
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.game_object.game_object import GameObject
from src.game_object.sprite import SpriteGroup
import src.scene.scene_manager as scene_manager


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


class Stage(Scene):
    def __init__(self, name: str, scene: StagedScene):
        super().__init__(name)
        self.scene = scene
        self.display = scene.display
        self.enabled = True
        self.group = SpriteGroup()

    def update(self) -> None:
        if not self.enabled:
            return
        self.group.update()

    def render(self) -> None:
        if not self.enabled:
            return
        self.group.render(self.display)


class StagedScene(Scene):
    def __init__(self, name: str):
        super().__init__(name)
        self._stages: list[Stage] = []

    def set_stage(self, stage: Stage):
        if self.current_stage:
            self.current_stage.enabled = False
        self._stages.append(stage)

    def exit_stage(self):
        self._stages.pop()
        self.current_stage.enabled = True

    @property
    def current_stage(self) -> Stage:
        if self._stages:
            return self._stages[-1]

    def render_stage(self):
        if self._stages:
            self.current_stage.render()

    def update_stage(self):
        if self._stages:
            self.current_stage.update()
