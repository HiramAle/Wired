import pygame
import src.engine.assets as game_assets
from src.utils.json_saver import instance as save_manager
from src.scene.pause_menu.book import Category
from src.game_object.sprite import SpriteGroup, Sprite
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.constants.colors import *
from src.scene.world.player import Player


class Inventory(Category):
    def __init__(self):
        super().__init__("Inventario")
        self.left_group = SpriteGroup()
        GUIText(save_manager.game_save.name, (109 + 14, 74), 32, self.left_group, centered=False, color=BLACK_SPRITE,
                shadow=False)
        GUIText(f"{save_manager.game_save.money}G", (241 + 14, 74), 32, self.left_group, centered=False,
                color=BLACK_SPRITE, shadow=False)
        GUIImage("character", (86 + 14, 80), game_assets.images_book["character"], self.left_group, centered=False)
        GUIImage("money", (217 + 14, 80), game_assets.images_book["money"], self.left_group, centered=False)

        self.player = Player((32, 48), [], [], [])
        self.player.action = "book"
        self.player_image = Sprite("p_i", (self.left_page.true_center_x, self.left_page.true_center_y),
                                   pygame.Surface((64, 96), pygame.SRCALPHA), self.left_group)

    def render(self, display: pygame.Surface):
        super().render(display)
        self.player_image.image = pygame.Surface((64, 96), pygame.SRCALPHA)
        self.player.animate()
        self.player_image.image.blit(pygame.transform.scale_by(self.player.image, 2), (0, 0))
        self.left_group.render(display)
