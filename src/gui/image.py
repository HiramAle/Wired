import pygame

from src.game_object.sprite import Sprite


class GUIImage(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, *groups, **extra):
        super().__init__(next((value for name, value in extra.items() if name == "name"), "image"), position, image,
                         *groups)
        for name, value in extra.items():
            match name:
                case "centered":
                    self.centered = value
