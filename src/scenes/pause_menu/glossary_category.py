import pygame
import engine.assets as game_assets
from src.utils.json_saver import instance as save_manager
from src.scenes.pause_menu.book import Category
from engine.objects.sprite import SpriteGroup
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.constants.colors import *


class Glossary(Category):
    def __init__(self):
        super().__init__("Glosario")
        self.left_group = SpriteGroup()
        GUIText(save_manager.game_save.name, (109 + 14, 74), 32, self.left_group, centered=False, color=BLACK_SPRITE,
                shadow=False)
        GUIText(f"{save_manager.game_save.money}G", (241 + 14, 74), 32, self.left_group, centered=False,
                color=BLACK_SPRITE, shadow=False)
        GUIImage("character", (86 + 14, 80), game_assets.images_book["character"], self.left_group, centered=False)
        GUIImage("money", (217 + 14, 80), game_assets.images_book["money"], self.left_group, centered=False)

    def render(self, display: pygame.Surface):
        super().render(display)
        self.left_group.render(display)
