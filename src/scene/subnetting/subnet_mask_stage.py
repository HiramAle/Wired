import pygame
import src.engine.input as game_input
import src.engine.time as game_time
import src.engine.assets as assets
from src.scene.core.scene import Stage, StagedScene
from src.game_object.sprite import SpriteGroup
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.scene.subnetting.zone_stage import Zone
from src.scene.subnetting.subnetting_objects import *
from src.constants.colors import WHITE_MOTION
from random import randint, shuffle


class SubnetMask(Stage):
    def __init__(self, scene: StagedScene, data: CustomMaskProblem):
        super().__init__("subnet_mask", scene)
        self.data = data
        self.class_positions = {"a": (401, 55), "b": (418, 112), "c": (403, 171)}
        self.answer_positions = [(448, 45), (515, 58), (459, 95), (525, 107), (454, 144), (515, 164)]
        self.default_masks = {"a": [255, 0, 0, 0], "b": [255, 255, 0, 0], "c": [255, 255, 255, 0]}
        self.holders_number = {"a": 3, "b": 2, "c": 1}
        self.df_positions = [()]

        self.possible_answers = self.data.correctAnswers + [randint(0, 255) for index in range(6 - self.data.blanks)]

        shuffle(self.possible_answers)

        self.zone = self.data.zone
        self.ip = self.data.ip

        self.group = SpriteGroup()
        self.class_labels = SpriteGroup()
        self.labels = SpriteGroup()
        self.df_labels = SpriteGroup()
        self.holders = SpriteGroup()
        self.cm_labels = SpriteGroup()
        # Images
        GUIImage("tab", (0, 0), assets.images_subnetting["subnet_mask_tab"], self.group, centered=False)
        GUIImage("sticker_holder", (362, 19), assets.images_subnetting["subnet_mask_holder"], self.group,
                 centered=False)
        GUIImage("post_it", (40, 251), assets.images_subnetting["post_it_class"], self.group, centered=False)
        # Underscore
        GUIImage("underscore_orange", (120, 176), assets.images_subnetting["underscore_orange"], self.group,
                 centered=False)
        GUIImage("underscore_yellow", (48, 208), assets.images_subnetting["underscore_yellow"], self.group,
                 centered=False)
        GUIImage("undescoreyellow", (220, 208), assets.images_subnetting["undescoreyellow"], self.group, centered=False)
        self.class_holder = GUIImage("class_holder", (67, 287), assets.images_subnetting["class_holder"], self.group,
                                     centered=False)

        # Texts
        GUIText(self.zone, (120, 185), 32, self.group, font="fool", centered=False, color="#2E2E2E", shadow=False)
        GUIText("Dirección IP:", (46, 215), 32, self.group, font="fool", centered=False, color="#2E2E2E", shadow=False)
        GUIText(self.ip, (287, 229), 32, self.group, font="fool", color="#2E2E2E", shadow=False)
        GUIText("Default mask:", (161, 260), 32, self.group, font="fool", color="#2E2E2E", shadow=False, centered=False)
        GUIText("Custom mask:", (157, 306), 32, self.group, font="fool", color="#2E2E2E", shadow=False, centered=False)
        GUIText("Clase", (62, 254), 32, self.group, font="fool", color="#2E2E2E", shadow=False, centered=False)

        self.continue_message = GUIText("Presiona la siguiente pestaña para\ncontinuar :-)", (478, 237), 16,
                                        shadow=False, color="#2E2E2E")

        for network_class, position in self.class_positions.items():
            ClassLabel(position, network_class, self.group, self.class_labels)

        for index, position in enumerate(self.answer_positions):
            Label((position[0] + 25, position[1] + 12.5), self.possible_answers[index], False, self.group, self.labels)

        for index in range(4):
            Label((340 + 25 + (index * 65), 262 + 13.5), "", True, self.group, self.df_labels)
            if index < 3:
                GUIText(".", (340 + 50 + 7.5 + (index * 65), 262 + 13.5), 32, self.group, font="fool", shadow=False,
                        color=DARK_BLACK_MOTION)

        tab_image = pygame.Surface((19, 54), pygame.SRCALPHA)
        self.tab = GUIImage("tab", (608, 77), tab_image, centered=False)

        self.dragging = False
        self.selected_label: ClassLabel | Label | None = None

        self.class_answer: ClassLabel | None = None
        self.group.add(*self.data.buildings)
        # TODO: Center zone name
        # TODO: Remove dots when class removed
        # TODO: Check swap class answer and labels
        self.drag_class = True

    def drag(self):
        # Start dragging
        if not self.dragging and game_input.mouse.buttons["left_hold"]:
            for label in self.class_labels.sprites() + self.labels.sprites():
                if label.rect.collidepoint(game_input.mouse.position):
                    if isinstance(label, ClassLabel) and not self.drag_class:
                        continue

                    if isinstance(label, Label):
                        if not label.can_move:
                            return
                    self.dragging = True

                    self.selected_label = label
                    self.selected_label.state = LabelStates.FULL
                    self.selected_label.layer = 1

                    if isinstance(self.selected_label, Label):
                        label.holder = None

                    break

        # On dragging
        if self.dragging:
            self.selected_label.y -= (self.selected_label.y - game_input.mouse.y) / (0.01 / game_time.dt)
            self.selected_label.x -= (self.selected_label.x - game_input.mouse.x) / (0.01 / game_time.dt)

        # End dragging
        if self.dragging and not game_input.mouse.buttons["left_hold"]:
            if isinstance(self.selected_label, ClassLabel):
                if self.class_holder.rect.collidepoint(game_input.mouse.position):

                    self.selected_label.position = self.class_holder.rect.center
                    self.class_answer = self.selected_label
                    default_mask = self.default_masks[self.class_answer.network_class]

                    for index, number in enumerate(default_mask):
                        self.df_labels.sprites()[index].value = number

                    for index in range(4 - self.holders_number[self.class_answer.network_class]):
                        Label((340 + 25 + (65 * index), 308 + 12.5), 255, True, self.group, self.cm_labels)

                    if not self.holders.sprites():
                        for index in range(self.holders_number[self.class_answer.network_class]):
                            x_padding = (3 - self.holders_number[self.class_answer.network_class]) * 65
                            LabelHolder((400 + x_padding + (index * 65), 301), self.group, self.holders)

                    for index in range(3):
                        GUIText(".", (340 + 50 + 7.5 + (index * 65), 308 + 13.5), 32, self.group, font="fool",
                                shadow=False,
                                color=DARK_BLACK_MOTION)

                    if self.class_answer.network_class == self.data.ipClass.lower():
                        self.class_holder.deactivate()
                        self.drag_class = False


                else:
                    self.class_answer = None
                    self.selected_label.position = self.class_positions[self.selected_label.network_class]
                    self.selected_label.state = LabelStates.STICK

                    for label in self.df_labels.sprites():
                        label: Label
                        label.value = ""

                    for sprite in self.holders.sprites():
                        sprite.kill()

                    for sprite in self.cm_labels.sprites():
                        sprite.kill()

                    for label in self.labels.sprites():
                        label: Label
                        if label.position != label.default_position:
                            label.holder = None
                            label.position = label.default_position

            elif isinstance(self.selected_label, Label):
                for holder in self.holders.sprites():
                    holder: LabelHolder
                    if holder.rect.collidepoint(game_input.mouse.position) and holder.active:
                        self.selected_label.holder = holder
                if not self.selected_label.holder:
                    self.selected_label.position = self.selected_label.default_position
                    self.selected_label.state = LabelStates.STICK
                self.selected_label.layer = 0

                used_holders = len([label.holder for label in self.labels.sprites() if label.holder])

                if not self.class_answer:
                    self.dragging = False
                    self.selected_label = None
                    return

                if self.holders_number[self.class_answer.network_class] == used_holders and not self.drag_class:
                    right_indexes = []
                    for index, answer in enumerate(self.get_answers()):
                        if self.data.correctAnswers[index] == answer:
                            right_indexes.append(index)

                    for index, holder in enumerate(self.holders.sprites()):
                        if index in right_indexes:
                            for label in self.labels.sprites():
                                if label.holder == holder:
                                    # label.remove(self.labels)
                                    label.can_move = False
                                    label.layer = 0
                            holder.deactivate()
                            # self.holders_number[self.class_answer.network_class] -= 1

                    print(self.data.correctAnswers)
                    print(self.get_answers())

                    if self.data.correctAnswers == self.get_answers():
                        self.continue_message.add(self.group)

            self.dragging = False
            self.selected_label = None

    def get_answers(self):
        answers = []
        for holder in self.holders.sprites():
            holder: LabelHolder
            for label in self.labels.sprites():
                label: Label
                print(label.layer)
                if label.holder == holder:
                    answers.append(str(label.value))

        return answers

    def update(self) -> None:
        self.group.update()
        # Tab
        if self.tab.clicked and self.continue_message in self.group.sprites():
            self.scene.set_stage(Zone(self.scene, self.data))
        # Get answers
        class_answer = ""
        label_answers = []
        if game_input.keyboard.keys["space"]:
            print(self.class_answer.network_class)
            class_answer = self.class_answer.network_class
            for holder in self.holders.sprites():
                holder: LabelHolder
                for label in self.labels.sprites():
                    label: Label
                    if label.holder == holder:
                        print(label.value)
                        label_answers.append(str(label.value))
            if class_answer == self.data.ipClass.lower() and label_answers == self.data.correctAnswers:
                print("good")
            else:
                print("bad")

        self.drag()

    def render(self) -> None:
        self.group.render(self.display)
