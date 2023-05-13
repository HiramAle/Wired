import pygame


class Trigger(pygame.Rect):
    def __init__(self, name: str, x: float, y: float, width: float, height: float):
        super().__init__(x, y, width, height)
        self.name = name

