import pygame

import src.engine.time as engine_time
from src.scene.core.scene import Scene
from src.game_object.sprite import Sprite
from src.constants.colors import *


class Circle(Sprite):
    def __init__(self, position: tuple):
        super().__init__("circle", position, pygame.Surface((32, 32)))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(BLUE_MOTION)


def lerp(start: float, target: float, time: float):
    return start + (target - start) * time


def quadratic_ease_out(t):
    return 1 - (1 - t) ** 2


class AnimationScene(Scene):
    def __init__(self):
        super().__init__("animation")
        self.start_x = 50
        self.end_x = 590

        self.circle = Circle((self.start_x, 180))

        self.rate = 1

    def update(self) -> None:
        elapsed_time = pygame.time.get_ticks() - self.start_time
        velocity = quadratic_ease_out(elapsed_time / 1000)
        if velocity <= 0:
            return
        self.circle.x = lerp(self.start_x, self.end_x, velocity)

    def render(self):
        self.display.fill(DARK_BLACK_MOTION)
        self.circle.render(self.display)
