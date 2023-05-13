import pygame

from engine.ui.ui_element import UIElement


class Image(UIElement):
    def __init__(self, position: tuple, image: pygame.Surface, *groups, **kwargs):
        super().__init__(position, image, *groups, **kwargs)
