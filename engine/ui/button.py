import pygame
from enum import Enum

from engine.ui.ui_element import UIElement


class Button(UIElement):
    class States(Enum):
        UP = 0
        DOWN = 1

    def __init__(self, position: tuple, image: pygame.Surface, parent: UIElement = None, *groups, **kwargs):
        super().__init__(position, image, parent, *groups, **kwargs)
