import pygame
from engine.assets import Assets
from engine.save_manager import instance as save_manager
from src.scenes.pause_menu.book import Category
from engine.objects.sprite import SpriteGroup
from engine.ui.text import Text
from engine.ui.image import Image
from engine.constants import Colors


class Jobs(Category):
    def __init__(self):
        super().__init__("Trabajos")
        self.left_group = SpriteGroup()
        Text((109 + 14, 74), save_manager.active_save.name, 32, Colors.SPRITE, self.left_group, centered=False,
             shadow=False)
        Text((241 + 14, 74), f"{save_manager.active_save.money}G", 32, Colors.SPRITE, self.left_group, centered=False,
             shadow=False)
        Image((86 + 14, 80), Assets.images_book["character"], self.left_group, centered=False)
        Image((217 + 14, 80), Assets.images_book["money"], self.left_group, centered=False)

    def render(self, display: pygame.Surface):
        super().render(display)
        self.left_group.render(display)