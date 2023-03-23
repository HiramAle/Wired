import math

import pygame
import src.engine.assets as assets
import src.engine.input as input
import src.engine.data as data
import src.scene.core.scene_manager as scene_manager
from src.scene.cables.crimp import CrimpCable
from random import choice, shuffle
from src.scene.core.scene import Scene
from src.gui.image import GUIImage
from src.game_object.sprite import SpriteGroup
from src.scene.cables.cable_objects import Cable


class OrderCable(Scene):
    def __init__(self):
        super().__init__("order_cable")
        self.group = SpriteGroup()
        # Cable Cover
        GUIImage("background", (0, 0), assets.images_cables["table"], self.group, layer=0, centered=False, scale=2)

        self.cable2 = GUIImage("cable_background", (222, 180), assets.images_cables["cable_cover_background"],
                               self.group, scale=2, layer=1)
        self.cable = GUIImage("cable_foreground", (60, 180), assets.images_cables["cable_cover_foreground"],
                              self.group, layer=4, scale=2)
        # Cables
        self.can_drag = True
        self.ordered = False
        self.cable_positions = []
        self.selected_cable = None
        self.dragging = False
        self.mouse_offset = 0
        self.standardName = choice(list(data.cable_data["standards"].keys()))
        self.cable_order = data.cable_data["standards"][self.standardName]
        self.cables = []

        shuffled_cables = self.cable_order.copy()

        for index, cable_name in enumerate(shuffled_cables):
            cable_position = (int(self.display.get_width() / 2), 40 + (index * 40))
            self.cable_positions.append(cable_position[1])
            color = cable_name.split("_")[1]
            self.cables.append(Cable(cable_position, color, cable_name, self.group, layer=2))

    def check_cable_order(self):
        actual_order = [cable.name for cable in self.cables]
        self.ordered = (actual_order == self.cable_order)

    def drag(self):
        if not self.can_drag:
            return
            # Start dragging
        if not self.dragging and input.mouse.buttons["left_hold"]:
            for cable in self.cables:
                if cable.rect.collidepoint(input.mouse.position):
                    self.dragging = True
                    self.selected_cable = cable
                    self.selected_cable.shadowActive = False
                    self.selected_cable.layer = 3
                    self.mouse_offset = input.mouse.y - cable.y
                    break

        # On dragging
        if self.dragging:
            distance = (self.selected_cable.y - input.mouse.y - self.mouse_offset) / 15
            self.selected_cable.y -= round(distance)

            selected_index = self.cables.index(self.selected_cable)
            for cable in self.cables:
                if cable == self.selected_cable:
                    continue
                if cable.rect.collidepoint(input.mouse.position):
                    swap_index = self.cables.index(cable)
                    cable.y = self.cable_positions[selected_index]
                    self.cables[selected_index], self.cables[swap_index] = \
                        self.cables[swap_index], self.cables[selected_index]

        # End dragging
        if self.dragging and not input.mouse.buttons["left_hold"]:
            self.selected_cable.y = self.cable_positions[self.cables.index(self.selected_cable)]
            self.selected_cable.shadowActive = True
            self.selected_cable.layer = 2
            self.selected_cable = None
            self.dragging = False
            self.check_cable_order()

    def start(self):
        pygame.mouse.set_visible(True)

    def update(self) -> None:
        self.group.update()
        self.drag()
        if self.ordered:
            self.can_drag = False
            if input.keyboard.keys["SPACE"]:
                scene_manager.change_scene(self, CrimpCable(self.standardName), swap=True)

    def render(self) -> None:
        self.group.render(self.display)
