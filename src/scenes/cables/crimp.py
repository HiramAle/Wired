import random
import pygame.mouse
from engine.assets import Assets
from engine.input import Input
from engine.time import Time
from src.scenes.cables.cable_objects import CrimpTool
from engine.objects.sprite import SpriteGroup
from engine.scene.scene import Scene
from engine.ui.text import Text
from engine.ui.image import Image
from engine.save_manager import instance as save_manager
from engine.constants import Colors


class CrimpCable(Scene):
    def __init__(self, cable_type: str):
        super().__init__("crimp_cable")
        self.standard = cable_type
        self.group = SpriteGroup()
        # Cable Cover
        Image((0, 0), Assets.images_cables["table"], self.group, layer=0, centered=False, scale=2)
        self.crimp_tool = CrimpTool((600, 180), self.group, layer=1)
        self.dragging = False
        self.mouse_offset = 0
        self.cable_rect = pygame.Rect(0, 0, 20, 20)
        self.cable_rect.center = (185, 180)
        self.magnetic_rect = pygame.Rect(0, 0, 100, 100)
        self.magnetic_rect.center = self.cable_rect.center
        self.cable_crimp = Image((0, self.center_y - 9), Assets.images_cables["crimp_cable"], self.group,
                                 centered=False)
        self.index = 1
        self.cable1 = Image((320 - 30, 400), Assets.images_cables["cable_icon"], self.group)
        self.cable2 = Image((320 + 30, 400), Assets.images_cables["cable_icon"], self.group)

        self.color_bar = Image((320, 40), Assets.images_cables["colorBar"], self.group)
        self.indicator = Image((self.color_bar.rect.right, 37), Assets.images_cables["indicator"], self.group)
        self.color_bar.deactivate()
        self.indicator.deactivate()
        self.movement = 300
        self.indicator_moving = True
        self.repositioning_tool = False
        self.adding_cable = False

        self.crimp_done = False
        self.continue_text = Text((self.center_x, 300), "Presiona Espacio para continuar", 32, Colors.WHITE, self.group,
                                  layer=10)
        self.continue_text.deactivate()
        cable_types = {"straight": "directo", "crossover": "cruzado"}
        self.result_cable_text = Text((self.center_x, 80),
                                      f"Felicidades!\nObtuviste un cable {cable_types[self.standard]}.",
                                      32, Colors.WHITE, self.group, layer=10)
        self.result_cable_text.deactivate()
        self.final_cable = Image((-150, self.center_y), Assets.images_cables[f"standard_a"], self.group)
        self.cable_quality = 0
        self.qualities = []
        self.color_values = {(101, 191, 110, 255): "green", (254, 202, 32, 255): "yellow", (222, 84, 81, 255): "red"}
        self.color_quality = {"green": 3, "yellow": 2, "red": 1}
        from engine.inventory import Inventory
        # print(f"player has usb? {Inventory.has('usb_double_cable')}")
        from engine.item_manager import ItemManager
        # print([ItemManager.get_item_by_id(item) for item in Inventory.items])
        self.cable_multiplier = random.choice([2] * 8 + [3] * 2) if Inventory.has("usb_double_cable") else 1
        # print(self.cable_multiplier)

    def drag(self):
        # Start dragging
        if not self.dragging and not self.repositioning_tool and not self.crimp_done:
            if self.crimp_tool.rect.collidepoint(Input.mouse.position) and Input.mouse.buttons["left"]:
                self.dragging = True
                pygame.mouse.set_visible(False)

        # On dragging
        if self.dragging:
            if self.crimp_tool.set:
                self.crimp_tool.move((self.cable_rect.centerx + 105, self.cable_rect.centery))
            else:
                self.crimp_tool.move((Input.mouse.x + 105, Input.mouse.y))

            if self.cable_rect.colliderect(self.crimp_tool.crimp_area) and not self.crimp_tool.playing:
                if self.magnetic_rect.collidepoint(Input.mouse.position):
                    self.crimp_tool.set = True
                    self.indicator_moving = True
                else:
                    self.crimp_tool.set = False

    def update(self) -> None:
        self.drag()
        self.group.update()

        if self.index == 2:
            self.cable1.y -= (self.cable1.y - 330) / (0.1 / Time.dt)
        elif self.index == 3 and not self.crimp_done:
            self.cable2.y -= (self.cable2.y - 330) / (0.1 / Time.dt)
            if self.cable2.y - 330 < 1:
                self.crimp_done = True

        # Repositions tool
        if self.repositioning_tool:
            self.crimp_tool.animation.rewind()
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
            if Input.mouse.buttons["left"]:
                color_x = int(self.indicator.x - self.color_bar.rect.left)
                # print(self.color_bar.image.get_at((color_x, self.color_bar.rect.centery)))
                color = self.color_values[tuple(self.color_bar.image.get_at((color_x, 9)))]
                self.qualities.append(self.color_quality[color])
                # self.qualities.append(self.color_quality[color])
                self.crimp_tool.playing = True
                self.indicator_moving = False

            # Reset
            if self.crimp_tool.playing and self.crimp_tool.animation.done:
                self.crimp_tool.set = False
                self.dragging = False
                self.repositioning_tool = True
                self.crimp_tool.animation.rewind()
                self.crimp_tool.animation.play()
                self.crimp_tool.playing = False
                self.index += 1
                if self.index == 3:
                    self.cable_crimp.deactivate()
                pygame.mouse.set_visible(True)

            # Updates Indicator position
            if self.indicator_moving:
                self.indicator.x += Time.dt * self.movement
                if self.indicator.x > self.color_bar.rect.right:
                    self.indicator.x = self.color_bar.rect.right
                    self.movement *= -1

                if self.indicator.x < self.color_bar.rect.left:
                    self.indicator.x = self.color_bar.rect.left
                    self.movement *= -1

        if self.crimp_done:
            self.crimp_tool.move((self.crimp_tool.x + 50, self.crimp_tool.y))
            self.cable1.y -= (self.cable1.y - 400) / (0.1 / Time.dt)
            self.cable2.y -= (self.cable2.y - 400) / (0.1 / Time.dt)

            self.final_cable.x -= (self.final_cable.x - 122) / (0.1 / Time.dt)
            if self.final_cable.x - 122 < 1:
                self.result_cable_text.activate()
                self.continue_text.activate()

            if Input.keyboard.keys["space"]:
                cable_quality = random.choice(self.qualities)
                from engine.inventory import Inventory
                Inventory.add_item(f"cable_{self.standard}_{cable_quality}", self.cable_multiplier)
                Inventory.remove_item("cable", 1)
                Inventory.remove_item("connector", 2)
                from engine.scene.scene_manager import SceneManager
                SceneManager.exit_scene()
        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            from src.scenes.pause_menu.pause import Pause
            SceneManager.change_scene(Pause())

    def start(self):
        pygame.mouse.set_visible(True)

    def render(self) -> None:
        self.group.render(self.display)
