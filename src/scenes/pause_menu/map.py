import pygame
from engine.assets import Assets
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup


class Map(Scene):
    def __init__(self):
        super().__init__("map")
        self.map = SpriteGroup()
        Sprite((4, 0), Assets.images_book["map"], self.map, centered=False)

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.map.render(self.display)
