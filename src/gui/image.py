import pygame

from src.game_object.sprite import Sprite


class GUIImage(Sprite):
    def __init__(self, name: str, position: tuple, image: pygame.Surface, *groups, **kwargs):
        super().__init__(name, position, image, *groups, **kwargs)
        print(name,kwargs)
