import pygame
from src.game_object.sprite import Sprite
from src.gui.text import GUIText
from src.constants.colors import *


class Blank(Sprite):
    def __init__(self, name: str, position: tuple, initial=False, *groups, **kwargs):
        super().__init__(name, position, pygame.Surface((64, 32)), *groups, **kwargs)
        self.image.set_colorkey((0, 0, 0))
        self.initial = initial
        if initial:
            self.empty = False
            pygame.draw.rect(self._image, DARK_BLACK_MOTION, pygame.Rect(0, 0, self.width, self.height),
                             border_radius=6, width=2)
        else:
            pygame.draw.rect(self._image, WHITE_MOTION, pygame.Rect(0, 0, self.width - 2, self.height - 2),
                             border_radius=6)
            self.empty = True


class Option(Sprite):
    def __init__(self, value: int, color: str | tuple, blank: Blank, *groups, **kwargs):
        super().__init__(f"option_{value}", blank.rect.center, pygame.Surface((60, 28)), *groups, **kwargs)
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self._image, color, pygame.Rect(0, 0, self.width, self.height), border_radius=4)
        self.text = GUIText(str(value), self.position, 32, *groups)
