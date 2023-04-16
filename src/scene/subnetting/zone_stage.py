import pygame
import src.engine.input as game_input
import src.engine.assets as assets
from src.scene.core.scene import Stage, StagedScene
from src.game_object.sprite import SpriteGroup
from src.gui.image import GUIImage
from src.scene.subnetting.subnetting_objects import *


class Zone(Stage):
    def __init__(self, scene: StagedScene, data: CustomMaskProblem):
        super().__init__("subnet_mask", scene)
        self.data = data
        self.group = SpriteGroup()
        self.buildings = SpriteGroup()
        self.selected_building: Building | None = None
        GUIImage("tab", (0, 0), assets.images_subnetting["zone_tab"], self.group, centered=False)

        tab_image = pygame.Surface((19, 54), pygame.SRCALPHA)
        self.tab = GUIImage("tab", (606, 19), tab_image, centered=False)

        GUIText("Dirección IP:", (46, 215), 32, self.group, font="fool", centered=False, color="#2E2E2E", shadow=False)
        GUIText(self.data.ip, (287, 229), 32, self.group, font="fool", color="#2E2E2E", shadow=False)

        map_padding_x = 266 / 4
        map_padding_y = 138 / 2
        for y in range(2):
            for x in range(4):
                if (x, y) in self.data.house_positions:
                    building_x = 57 + (map_padding_x * x) + map_padding_x / 2
                    building_y = 29 + (map_padding_y * y) + map_padding_y / 2
                    Building((building_x, building_y), "house", self.group, self.buildings)

    def update(self) -> None:
        if self.tab.clicked:
            self.scene.exit_stage()

        for building in self.buildings.sprites():
            building: Building
            if building.clicked:
                building.selected = True
                if self.selected_building:
                    self.selected_building.selected = False
                self.selected_building = building

    def render(self) -> None:
        self.group.render(self.display)
