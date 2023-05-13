import pygame

from engine.objects.sprite import Sprite


class UIElement(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface = None, *groups, **kwargs):
        super().__init__(position, image, *groups, **kwargs)
        self.parent = None

        for key, val in kwargs.items():
            if key in ["parent"] and hasattr(self, key):
                setattr(self, key, val)
