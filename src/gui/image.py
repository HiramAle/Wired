import pygame

from engine.objects.sprite import Sprite


class GUIImage(Sprite):
    def __init__(self, name: str, position: tuple, image: pygame.Surface, *groups, **kwargs):
        super().__init__(name, position, image, *groups, **kwargs)
