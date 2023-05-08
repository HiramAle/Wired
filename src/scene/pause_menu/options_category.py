import pygame
import src.engine.assets as game_assets
from src.utils.json_saver import instance as save_manager
from src.scene.pause_menu.book import Category
from src.game_object.sprite import SpriteGroup
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.constants.colors import *


class Options(Category):
    def __init__(self):
        super().__init__("Opciones")
        self.left_group = SpriteGroup()
        self.right_group = SpriteGroup()
        GUIText("Controles", (465, 42), 32, self.right_group, shadow=False, color=BLACK_SPRITE)
        print(self.right_page.canvas.get_rect(topleft=self.right_page.position).centerx)

    def render(self, display: pygame.Surface):
        super().render(display)
        self.left_group.render(display)
        self.right_group.render(display)
