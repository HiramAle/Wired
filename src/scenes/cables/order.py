import pygame
from engine.assets import Assets
from engine.input import Input
from engine.data import Data
from engine.time import Time
from engine.window import Window
from src.scenes.cables.crimp import CrimpCable
from random import choice, shuffle
from engine.scene.scene import Scene
from engine.ui.image import Image
from engine.objects.sprite import SpriteGroup
from src.scenes.cables.cable_objects import Cable
from engine.ui.text import Text
from engine.constants import Colors
from src.scenes.tutorial.tutorial import Tutorial


class OrderCable(Scene):
    def __init__(self):
        super().__init__("order_cable")
        self.group = SpriteGroup()
        # Cable Cover
        Image((0, 0), Assets.images_cables["table"], self.group, layer=0, centered=False, scale=2)

        self.cable2 = Image((222, 180), Assets.images_cables["cable_cover_background"],
                            self.group, scale=2, layer=1)
        self.cable = Image((60, 180), Assets.images_cables["cable_cover_foreground"],
                           self.group, layer=4, scale=2)
        # Cables
        self.can_drag = True
        self.ordered = False
        self.cable_positions = []
        self.selected_cable = None
        self.dragging = False
        self.standardName = choice(list(Data.cable_data["standards"].keys()))
        self.cable_order = Data.cable_data["standards"][self.standardName]
        self.cables = []

        shuffled_cables = self.cable_order.copy()
        # shuffle(shuffled_cables)

        for index, cable_name in enumerate(shuffled_cables):
            cable_position = (int(self.display.get_width() / 2), 40 + (index * 40))
            self.cable_positions.append(cable_position[1])
            color = cable_name.split("_")[1]
            self.cables.append(Cable(cable_position, color, cable_name, self.group, layer=2))

        self.cable_swap: Cable = None
        self.cable_swap_position = 0

        self.cable_swaps: list[Cable] = []
        self.cable_swaps_positions = []

        self.tutorial = False

        self.text = Text((self.center_x, 300), "Presiona Espacio para continuar", 32, Colors.WHITE, self.group,
                         layer=10)
        self.text.opacity = 0
        Text((562, self.center_y - 10), "Estandard", 32, Colors.WHITE, self.group, layer=10)
        Text((562, self.center_y + 10), self.standardName, 32, Colors.WHITE, self.group, layer=10)


    def check_cable_order(self):
        if self.tutorial:
            for index, cable in enumerate(self.cables):
                if cable.name == self.cable_order[index]:
                    cable.right_order = True
                else:
                    cable.right_order = False
        actual_order = [cable.name for cable in self.cables]
        self.ordered = (actual_order == self.cable_order)

    def drag(self):
        if not self.can_drag:
            return
            # Start dragging
        if not self.dragging and Input.mouse.buttons["left_hold"]:
            for cable in self.cables:
                if cable.rect.collidepoint(Input.mouse.position):
                    self.dragging = True
                    self.selected_cable = cable
                    self.selected_cable.shadowActive = False
                    self.selected_cable.layer = 3
                    self.selected_cable.dragging = True
                    break

        # On dragging
        if self.dragging:
            # TODO: Limit the height of the drag
            self.selected_cable.y -= (self.selected_cable.y - Input.mouse.y) / (0.05 / Time.dt)
            selected_index = self.cables.index(self.selected_cable)
            for cable in self.cables:
                if cable == self.selected_cable or cable.swapping:
                    continue
                if cable.rect.collidepoint(Input.mouse.position):
                    swap_index = self.cables.index(cable)
                    cable.swap(self.cable_positions[selected_index])
                    self.cables[selected_index], self.cables[swap_index] = \
                        self.cables[swap_index], self.cables[selected_index]

        # End dragging
        if self.dragging and not Input.mouse.buttons["left_hold"]:
            self.selected_cable.swap(self.cable_positions[self.cables.index(self.selected_cable)])
            self.selected_cable.shadowActive = True
            self.selected_cable.layer = 2
            self.selected_cable.dragging = False
            self.selected_cable = None
            self.dragging = False
            self.check_cable_order()

    def start(self):
        pygame.mouse.set_visible(True)

    def update(self) -> None:
        self.group.update()
        self.drag()

        # Change cursor while the cables are not ordered
        if any([cable.hovered for cable in self.cables]) and not self.ordered:
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

        if self.ordered:
            self.text.opacity = 255
            self.can_drag = False
            if Input.keyboard.keys["space"]:
                from engine.scene.scene_manager import SceneManager
                SceneManager.change_scene(CrimpCable(self.standardName), swap=True, transition=True)
        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            from src.scenes.pause_menu.pause import Pause
            SceneManager.change_scene(Pause())

    def render(self) -> None:
        self.group.render(self.display)
