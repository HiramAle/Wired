import random

import pygame.mouse
import src.engine.assets as assets
import src.engine.input as input
import src.engine.time as time
from src.scene.cables.cable_objects import CrimpTool
from src.game_object.sprite import SpriteGroup
from src.scene.core.scene import Scene
from src.gui.image import GUIImage
from src.gui.text import GUIText


class CrimpCable(Scene):
    def __init__(self, standard: str):
        super().__init__("crimp_cable")
        self.standard = standard
        self.group = SpriteGroup()
        # Cable Cover
        GUIImage("background", (0, 0), assets.images_cables["table"], self.group, layer=0, centered=False, scale=2)
        self.crimp_tool = CrimpTool((600, 180), assets.animations["cables"]["crimp"], self.group, layer=1)
        self.dragging = False
        self.mouse_offset = 0
        self.cable_rect = pygame.Rect(0, 0, 20, 20)
        self.cable_rect.center = (185, 180)
        self.magnetic_rect = pygame.Rect(0, 0, 100, 100)
        self.magnetic_rect.center = self.cable_rect.center
        self.cable_crimp = GUIImage("crimp_cable", (0, self.center_y - 9), assets.images_cables["crimp_cable"],
                                    self.group,
                                    centered=False)
        self.index = 1
        self.cable1 = GUIImage("crimp_cable", (320 - 30, 400), assets.images_cables["cable_icon"], self.group)
        self.cable2 = GUIImage("crimp_cable", (320 + 30, 400), assets.images_cables["cable_icon"], self.group)

        self.color_bar = GUIImage("color_bar", (320, 40), assets.images_cables["colorBar"], self.group)
        self.indicator = GUIImage("indicator", (self.color_bar.rect.right, 37), assets.images_cables["indicator"],
                                  self.group)
        self.color_bar.deactivate()
        self.indicator.deactivate()
        self.movement = 200
        self.indicator_moving = True
        self.repositioning_tool = False
        self.adding_cable = False

        self.crimp_done = False
        self.continue_text = GUIText("Presiona Espacio para continuar", (self.center_x, 300), 32, self.group, layer=10)
        self.continue_text.deactivate()
        self.standard_text = GUIText(self.standard, self.center, 32, self.group, layer=10)
        self.standard_text.deactivate()
        self.final_cable = GUIImage("final", (-150, self.center_y),
                                    assets.images_cables[f"standard_{self.standard.lower()[-1]}"], self.group)

    def drag(self):
        # Start dragging
        if not self.dragging and not self.repositioning_tool and not self.crimp_done:
            if self.crimp_tool.rect.collidepoint(input.mouse.position) and input.mouse.buttons["left"]:
                self.dragging = True
                pygame.mouse.set_visible(False)

        # On dragging
        if self.dragging:
            if self.crimp_tool.set:
                self.crimp_tool.move((self.cable_rect.centerx + 105, self.cable_rect.centery))
            else:
                self.crimp_tool.move((input.mouse.x + 105, input.mouse.y))

            if self.cable_rect.colliderect(self.crimp_tool.crimp_area) and not self.crimp_tool.playing:
                if self.magnetic_rect.collidepoint(input.mouse.position):
                    self.crimp_tool.set = True
                    self.indicator_moving = True
                else:
                    self.crimp_tool.set = False

    def update(self) -> None:
        self.drag()
        self.group.update()

        if self.index == 2:
            self.cable1.y -= (self.cable1.y - 330) / (0.1 / time.dt)
        elif self.index == 3 and not self.crimp_done:
            self.cable2.y -= (self.cable2.y - 330) / (0.1 / time.dt)
            if self.cable2.y - 330 < 1:
                self.crimp_done = True

        # Repositions tool
        if self.repositioning_tool:
            self.crimp_tool.move((600, 180))
            if abs(600 - self.crimp_tool.x) <= 1 and abs(180 - self.crimp_tool.y) <= 1:
                self.crimp_tool.x = 600
                self.crimp_tool.y = 180
                self.repositioning_tool = False

        if not self.crimp_tool.set:
            # Deactivate color bar and indicator
            self.color_bar.deactivate()
            self.indicator.deactivate()
            # Reset the indicator position
            self.indicator.x = random.choice(
                [self.color_bar.rect.right, self.color_bar.rect.left, self.color_bar.rect.centerx])
        else:
            # Activate color bar and indicator
            self.indicator.activate()
            self.color_bar.activate()

            # Play animation if mouse left button pressed
            if input.mouse.buttons["left"]:
                self.crimp_tool.playing = True
                self.indicator_moving = False

            # Reset
            if self.crimp_tool.playing and self.crimp_tool.done:
                self.crimp_tool.set = False
                self.dragging = False
                self.repositioning_tool = True
                self.crimp_tool.rewind()
                self.crimp_tool.playing = False
                self.index += 1
                if self.index == 3:
                    self.cable_crimp.deactivate()
                pygame.mouse.set_visible(True)

            # Updates Indicator position
            if self.indicator_moving:
                self.indicator.x += time.dt * self.movement
                if self.indicator.x > self.color_bar.rect.right:
                    self.indicator.x = self.color_bar.rect.right
                    self.movement *= -1

                if self.indicator.x < self.color_bar.rect.left:
                    self.indicator.x = self.color_bar.rect.left
                    self.movement *= -1

        if self.crimp_done:
            self.crimp_tool.move((self.crimp_tool.x + 50, self.crimp_tool.y))
            self.cable1.y -= (self.cable1.y - 400) / (0.1 / time.dt)
            self.cable2.y -= (self.cable2.y - 400) / (0.1 / time.dt)

            self.final_cable.x -= (self.final_cable.x - 122) / (0.1 / time.dt)
            if self.final_cable.x - 122 < 1:
                self.standard_text.activate()
                self.continue_text.activate()

    def start(self):
        pygame.mouse.set_visible(True)

    def render(self) -> None:
        self.group.render(self.display)
