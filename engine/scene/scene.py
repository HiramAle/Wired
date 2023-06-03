from __future__ import annotations
import pygame
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from typing import Optional
from engine.objects.sprite import SpriteGroup
from engine.input import Input
from engine.window import Window


class Scene:
    def __init__(self, name: Optional[str]):
        self.name = name if name else self.__class__.__name__
        self.display = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)
        self.transitionPosition: tuple = self.center
        self.interactive = SpriteGroup()

    def update_cursor(self):
        if any([sprite.hovered for sprite in self.interactive.sprites()]):
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

    def start(self):
        ...

    @property
    def center_x(self):
        return self.display.get_size()[0] / 2

    @property
    def center_y(self):
        return self.display.get_size()[1] / 2

    @property
    def center(self) -> tuple:
        return self.center_x, self.center_y

    def update(self) -> None:
        ...

    def render(self) -> None:
        ...


class Stage(Scene):
    def __init__(self, name: str, scene: StagedScene):
        super().__init__(name)
        self.scene = scene
        self.display = scene.display


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
