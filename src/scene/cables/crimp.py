import pygame.mouse
import src.engine.assets as assets
import src.engine.input as input
import src.engine.time as time
from src.scene.cables.cable_objects import CrimpTool
from src.game_object.sprite import SpriteGroup
from src.scene.core.scene import Scene
from src.gui.image import GUIImage


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
        self.cable_rect.center = (200, 180)
        self.magnetic_rect = pygame.Rect(0, 0, 100, 100)
        self.magnetic_rect.center = self.cable_rect.center
        GUIImage("crimp_cable", (200, 180), assets.images_cables["crimp_cable"], self.group)
        self.index = 1
        self.cable1 = GUIImage("crimp_cable", (320 - 30, 330), assets.images_cables["StandardA"], self.group,
                               scale=0.25)
        self.cable2 = GUIImage("crimp_cable", (320 + 30, 330), assets.images_cables["StandardA"], self.group,
                               scale=0.25)
        self.cable1.deactivate()
        self.cable2.deactivate()

        self.color_bar = GUIImage("color_bar", (320, 40), assets.images_cables["colorBar"], self.group)
        self.indicator = GUIImage("indicator", (self.color_bar.rect.right, 37), assets.images_cables["indicator"],
                                  self.group)

        self.color_bar.deactivate()
        self.indicator.deactivate()

        self.movement = 100
        self.indicator_moving = True

    def drag(self):
        if not self.dragging and input.mouse.buttons["left"]:
            if self.crimp_tool.rect.collidepoint(input.mouse.position):
                self.dragging = True
                self.crimp_tool.moving = True
                self.mouse_offset = input.mouse.y - self.crimp_tool.y
                pygame.mouse.set_visible(False)

        # On dragging
        if self.dragging:
            distance_x = self.crimp_tool.x - input.mouse.x - 130
            distance_y = self.crimp_tool.y - input.mouse.y

            self.crimp_tool.x -= int(distance_x / 10)
            self.crimp_tool.y -= int(distance_y / 10)

        # End dragging
        if self.cable_rect.colliderect(self.crimp_tool.collider):
            if self.magnetic_rect.collidepoint(input.mouse.position):
                self.crimp_tool.re_position(self.cable_rect)
                self.crimp_tool.moving = False
                self.indicator.activate()
                self.color_bar.activate()
                self.crimp_tool.moving = True
            else:
                self.crimp_tool.moving = True
                self.color_bar.deactivate()
                self.indicator.deactivate()
                self.indicator_moving = False

            if input.mouse.buttons["left"]:
                self.crimp_tool.rewind()
                self.dragging = False
                self.indicator_moving = False
                print(self.color_bar.image.get_at((int(self.indicator.x - self.color_bar.rect.left), 9)))

            if self.crimp_tool.actual_frame >= len(self.crimp_tool.frames) - 1:
                self.crimp_tool.position = (600, 180)
                self.crimp_tool.actual_frame = 0
                self.crimp_tool.moving = True
                pygame.mouse.set_visible(True)
                if self.index == 1:
                    self.cable1.activate()
                if self.index == 2:
                    self.cable2.activate()
                self.index += 1
                self.color_bar.deactivate()
                self.indicator.deactivate()
                self.indicator_moving = True

    def update(self) -> None:
        self.drag()
        self.group.update()
        if self.indicator_moving:
            self.indicator.x += time.dt * self.movement

            if self.indicator.x > self.color_bar.rect.right:
                self.indicator.x = self.color_bar.rect.right
                self.movement *= -1

            if self.indicator.x < self.color_bar.rect.left:
                self.indicator.x = self.color_bar.rect.left
                self.movement *= -1

    def start(self):
        pygame.mouse.set_visible(True)

    def render(self) -> None:
        self.display.fill("black")
        self.group.render(self.display)

        pygame.draw.rect(self.display, "CYAN", self.cable_rect, 2)
        pygame.draw.rect(self.display, "BLUE", self.magnetic_rect, 2)
        pygame.draw.rect(self.display, "PINK", self.crimp_tool.collider, 2)
