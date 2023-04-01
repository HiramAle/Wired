import pygame

import src.engine.assets as assets
import src.engine.input as input
import src.engine.time as time
from src.scene.core.scene import StagedScene
from src.scene.subnetting.subnetting_objects import Option, Blank
from src.game_object.sprite import SpriteGroup
from src.constants.colors import BLUE_MOTION
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.constants.colors import *


class Subnetting(StagedScene):
    def __init__(self):
        super().__init__("subnetting")
        self.group = SpriteGroup()
        # GUIText("CLASE", (458, 36), 32, self.group)
        map_image = assets.images_subnetting["base_map"].convert_alpha()
        mask = pygame.mask.from_surface(map_image)
        shadow_map = mask.to_surface(setcolor=DARK_BLACK_MOTION, unsetcolor=(0, 0, 0))
        shadow_map.set_colorkey((0, 0, 0))
        shadow_map.set_alpha(70)
        GUIImage("shadow_map", (9, 14), shadow_map, self.group, centered=False)
        GUIImage("base_map", (13, 18), map_image, self.group, centered=False)

        # self.blanks: list[Blank] = []
        # for i in range(3):
        #     self.blanks.append(Blank("blank", (458, 100 + (40 * i)), True, self.group))
        #
        # for blank in self.blanks:
        #     Option(0, "RED", blank, self.group)
        #
        # self.dragging = False
        # self.selected_option: Option = None

    # def drag(self):
        # Start dragging
        # if not self.dragging and input.mouse.buttons["left_hold"]:
        #     for sprite in self.group.sprites:
        #         if isinstance(sprite, Option):
        #             if sprite.rect.collidepoint(input.mouse.position):
        #                 sprite.dragging = True
        #                 self.selected_option = sprite
        #                 self.dragging = True

        # End dragging
        # if self.dragging and not input.mouse.buttons["left_hold"]:
        #     self.selected_option.dragging = False
        #     self.dragging = False

    def start(self):
        pygame.mouse.set_visible(True)

    def update(self) -> None:
        self.group.update()

    def render(self) -> None:
        self.display.fill("#EEEEEE")
        self.group.render(self.display)
