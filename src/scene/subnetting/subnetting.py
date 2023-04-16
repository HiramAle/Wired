import pygame
import src.engine.assets as assets
import src.engine.input as input
import src.engine.time as time
from src.scene.core.scene import StagedScene
from src.scene.subnetting.subnetting_objects import *
from src.game_object.sprite import SpriteGroup
from src.constants.colors import BLUE_MOTION
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.constants.colors import *
from random import choice
from src.scene.subnetting.subnet_mask_stage import SubnetMask


class Subnetting(StagedScene):
    def __init__(self):
        super().__init__("subnetting")
        pygame.mouse.set_visible(True)
        zones = ["Laboratorio", "Escuela", "Oficina"]
        self.problemData = CustomMaskProblem(choice(zones))
        self.group = SpriteGroup()
        self.buildings = SpriteGroup()
        background_image = assets.images_subnetting[f"notebook_{choice(['blue', 'red', 'brown'])}"]
        GUIImage("background", (0, 0), background_image, self.group, centered=False)
        GUIImage("base_map", (40, 18), assets.images_subnetting["base_map"], self.group, centered=False)
        GUIImage("map", (57, 29), assets.images_subnetting["map"], self.group, centered=False)
        # Fill houses
        while len(self.problemData.house_positions) < self.problemData.subnetsNeeded:
            x = randint(0, 3)
            y = randint(0, 1)
            position = (x, y)
            if position not in self.problemData.house_positions:
                self.problemData.house_positions.append(position)
        self.set_stage(SubnetMask(self, self.problemData))

    def update(self) -> None:
        self.group.update()
        self.current_stage.update()

    def render(self) -> None:
        self.display.fill("#242424")
        self.group.render(self.display)
        self.current_stage.render()
