import pygame
from src.constants.colors import WHITE_MOTION
from src.game_object.sprite import Sprite
from src.game_object.components import Animation


class Entity(Sprite):
    def __init__(self, name: str, position: tuple, *groups, **kwargs):
        super().__init__(name, position, pygame.Surface((32, 32)), *groups, **kwargs)
        self.image.fill(WHITE_MOTION)
