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
from engine.playerdata import PlayerData


class OrderCable(Scene):
    def __init__(self, prev_order="?"):
        super().__init__("order_cable")
        print(f"Previous order: {prev_order}")
        self.group = SpriteGroup()
        # ----- PARAMS -----
        # straight or crossover
        self.previous_order = prev_order
        self.current_order = ""
        self.last_cable = True if prev_order != "?" else False

        # Cable Cover
        Image((0, 0), Assets.images_cables["table"], self.group, layer=0, centered=False, scale=2)

        self.cable2 = Image((222, 180), Assets.images_cables["cable_cover_background"],
                            self.group, scale=2, layer=1)
        self.cable = Image((60, 180), Assets.images_cables["cable_cover_foreground"],
                           self.group, layer=4, scale=2)
        self.cable_a = Data.cable_data["A"]
        self.cable_b = Data.cable_data["B"]
        # Cables
        self.can_drag = True
        self.ordered = False
        self.cable_positions = []
        self.selected_cable = None
        self.dragging = False
        # self.standardName = choice(list(Data.cable_data["standards"].keys()))
        # self.cable_order = Data.cable_data[self.required_order]
        self.cables = []

        shuffled_cables = Data.cable_data["A"].copy()
        shuffle(shuffled_cables)

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

        self.instructions_text = Text((self.center_x, 300), "Presiona Espacio para continuar", 32, Colors.WHITE,
                                      self.group, layer=10)
        self.instructions_text.deactivate()
        Text((562, self.center_y - 10), "Estandard", 32, Colors.WHITE, self.group, layer=10)
        self.standard_text = Text((562, self.center_y + 10), "?", 32, Colors.WHITE, self.group, layer=10)

    def check_cable_order(self):
        # if self.tutorial:
        #     for index, cable in enumerate(self.cables):
        #         if cable.name == self.cable_order[index]:
        #             cable.right_order = True
        #         else:
        #             cable.right_order = False

        actual_order = [cable.name for cable in self.cables]
        if actual_order == self.cable_a:
            self.ordered = True
            self.current_order = "A"
        elif actual_order == self.cable_b:
            self.ordered = True
            self.current_order = "B"
        else:
            self.current_order = "?"
            self.ordered = False
            self.instructions_text.deactivate()
        self.standard_text.text = self.current_order

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
        if any([cable.hovered for cable in self.cables]):
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

        if self.ordered:
            self.instructions_text.activate()
            # self.can_drag = False
            if Input.keyboard.keys["space"]:
                from engine.scene.scene_manager import SceneManager
                if self.last_cable:
                    combination = f"{self.previous_order}{self.current_order}"
                    cable_type = "crossover" if combination in ["AB", "BA"] else "straight"
                    SceneManager.change_scene(CrimpCable(cable_type), swap=True, transition=True)
                else:
                    if self.current_order == "A":
                        SceneManager.change_scene(OrderCable("A"), swap=True, transition=True)
                    elif self.current_order == "B":
                        SceneManager.change_scene(OrderCable("B"), swap=True, transition=True)

        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            from src.scenes.pause_menu.pause import Pause
            SceneManager.change_scene(Pause())


    def render(self) -> None:
        self.group.render(self.display)
