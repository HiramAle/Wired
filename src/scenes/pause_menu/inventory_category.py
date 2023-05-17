import pygame
from engine.assets import Assets
from engine.save_manager import instance as save_manager
from src.scenes.pause_menu.book import Category
from engine.objects.sprite import SpriteGroup, Sprite
from engine.ui.text import Text
from engine.ui.image import Image
from src.constants.colors import *
from src.scenes.world.player import Player
from engine.constants import Colors


class Inventory(Category):
    def __init__(self):
        super().__init__("Inventario")
        self.left_group = SpriteGroup()
        Text((109 + 14, 74), save_manager.active_save.name, 32, Colors.SPRITE, self.left_group, centered=False,
             shadow=False)
        Text((241 + 14, 74), f"{save_manager.active_save.money}G", 32, Colors.WHITE, self.left_group, centered=False,
             shadow=False)
        Image((86 + 14, 80), Assets.images_book["character"], self.left_group, centered=False)
        Image((217 + 14, 80), Assets.images_book["money"], self.left_group, centered=False)

        self.player = Player((32, 48), [], [], [])
        self.player.action = "book"
        self.player_image = Sprite((169, 173), pygame.Surface((64, 96), pygame.SRCALPHA), self.left_group)

    def render(self, display: pygame.Surface):
        super().render(display)
        self.player_image.image = pygame.Surface((64, 96), pygame.SRCALPHA)
        self.player.animate()
        self.player_image.image.blit(pygame.transform.scale_by(self.player.image, 2), (0, 0))
        self.left_group.render(display)
