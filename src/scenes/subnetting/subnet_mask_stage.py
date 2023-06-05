from engine.scene.scene import Stage, StagedScene
from engine.objects.sprite import SpriteGroup
from engine.ui.image import Image
from src.scenes.subnetting.zone_stage import Zone
from src.scenes.subnetting.subnetting_objects import *
from random import randint, shuffle
from engine.data import Data


class SubnetMask(Stage):
    def __init__(self, scene: StagedScene, zone_id: str, interactive: SpriteGroup):
        super().__init__("subnet_mask", scene)
        self.data = Data.subnetting[zone_id]
        self.class_positions = {"a": (401, 55), "b": (418, 112), "c": (403, 171)}
        self.answer_positions = [(448, 45), (515, 58), (459, 95), (525, 107), (454, 144), (515, 164)]
        self.default_masks = {"a": [255, 0, 0, 0], "b": [255, 255, 0, 0], "c": [255, 255, 255, 0]}
        self.holders_number = {"a": 3, "b": 2, "c": 1}
        self.df_positions = [()]

        self.possible_answers = self.data.correctAnswers + [randint(0, 255) for index in range(6 - self.data.blanks)]

        shuffle(self.possible_answers)

        self.zone = self.data.zone_name
        self.ip = self.data.ip

        self.group = SpriteGroup()
        self.class_labels = SpriteGroup()
        self.labels = SpriteGroup()
        self.df_labels = SpriteGroup()
        self.holders = SpriteGroup()
        self.cm_labels = SpriteGroup()
        # Images
        Image((0, 0), Assets.images_subnetting["subnet_mask_tab"], self.group, interactive,centered=False)
        Image((362, 19), Assets.images_subnetting["subnet_mask_holder"], self.group,
              centered=False)
        Image((40, 251), Assets.images_subnetting["post_it_class"], self.group, centered=False)
        # Underscore
        Image((120, 176), Assets.images_subnetting["underscore_orange"], self.group,
              centered=False)
        Image((48, 208), Assets.images_subnetting["underscore_yellow"], self.group,
              centered=False)
        Image((220, 208), Assets.images_subnetting["undescoreyellow"], self.group, centered=False)
        self.class_holder = Image((67, 287), Assets.images_subnetting["class_holder"], self.group,
                                  centered=False)

        # Texts
        Text((120, 185), self.zone, 32, "#2E2E2E", self.group, font="fool", centered=False, shadow=False)
        Text((46, 215), "Dirección IP:", 32, "#2E2E2E", self.group, font="fool", centered=False, shadow=False)
        Text((287, 229), self.ip, 32, "#2E2E2E", self.group, font="fool", shadow=False)
        Text((161, 260), "Default mask:", 32, "#2E2E2E", self.group, font="fool", shadow=False, centered=False)
        Text((157, 306), "Custom mask:", 32, "#2E2E2E", self.group, font="fool", shadow=False, centered=False)
        Text((62, 254), "Clase", 32, "#2E2E2E", self.group, font="fool", shadow=False, centered=False)

        self.continue_message = Text((478, 237), "Presiona la siguiente pestaña para\ncontinuar :-)", 16, "#2E2E2E",
                                     shadow=False)

        for network_class, position in self.class_positions.items():
            ClassLabel(position, network_class, self.group, self.class_labels, interactive)

        for index, position in enumerate(self.answer_positions):
            Label((position[0] + 25, position[1] + 12.5), self.possible_answers[index], False, self.group, self.labels,
                  interactive)

        for index in range(4):
            Label((340 + 25 + (index * 65), 262 + 13.5), "", True, self.group, self.df_labels)
            if index < 3:
                Text((340 + 50 + 7.5 + (index * 65), 262 + 13.5), ".", 32, Colors.DARK, self.group, font="fool",
                     shadow=False)

        tab_image = pygame.Surface((19, 54), pygame.SRCALPHA)
        self.tab = Image((608, 77), tab_image, centered=False)

        self.dragging = False
        self.selected_label: ClassLabel | Label | None = None

        self.class_answer: ClassLabel | None = None
        self.group.add(*self.data.buildings)
        # TODO: Center zone name
        # TODO: Remove dots when class removed
        # TODO: Check swap class answer and labels
        self.drag_class = True

        self.can_drag = True

    def clear_default_labels(self):
        for label in self.df_labels.sprites():
            label: Label
            label.value = ""

    def set_default_labels(self):
        for index, label in enumerate(self.df_labels.sprites()):
            label: Label
            label.value = self.default_masks[self.class_answer.network_class][index]

    def clear_holders(self):
        for sprite in self.holders.sprites():
            sprite.kill()

    def set_holders(self):
        for index in range(self.holders_number[self.class_answer.network_class]):
            x_padding = (3 - self.holders_number[self.class_answer.network_class]) * 65
            LabelHolder((400 + x_padding + (index * 65), 301), self.group, self.holders)

    def set_custom_labels(self):
        for index in range(4 - self.holders_number[self.class_answer.network_class]):
            Label((340 + 25 + (65 * index), 308 + 12.5), 255, True, self.group, self.cm_labels)

    def clear_custom_labels(self):
        for label in self.cm_labels.sprites():
            label.kill()

    def set_points(self):
        for index in range(3):
            Text((340 + 50 + 7.5 + (index * 65), 308 + 13.5), ".", 32, Colors.DARK, self.group, font="fool",
                 shadow=False)

    def clear_points(self):
        for sprite in [sprite for sprite in self.group.sprites() if isinstance(sprite, Text)]:
            if sprite.text == ".":
                sprite.kill()

    def reposition_answers(self):
        for label in self.labels.sprites():
            label: Label
            if label.holder:
                label.holder.label = None
                label.holder = None
            label.reposition()

    def start_dragging_class(self):
        if not self.can_drag:
            return
        # If is dragging, cant start dragging
        if self.dragging:
            return
        # If it is not dragging but player doesn't press left hold, cant start dragging
        if not Input.mouse.buttons["left_hold"]:
            return
        # If it can dragg class check for class labels
        for class_label in self.class_labels.sprites():
            class_label: ClassLabel
            if class_label.rect.collidepoint(Input.mouse.position):
                self.dragging = True
                self.selected_label = class_label
                self.selected_label.state = LabelStates.FULL

    def start_dragging_answer(self):
        if not self.can_drag:
            return
        # If is dragging, cant start dragging
        if self.dragging:
            return
        # If it is not dragging but player doesn't press left hold, cant start dragging
        if not Input.mouse.buttons["left_hold"]:
            return
        # If class label is set, can dragg answer labels
        if not self.class_answer:
            return

        for label in self.labels.sprites():
            label: Label
            if label.rect.collidepoint(Input.mouse.position):
                self.dragging = True
                self.selected_label = label
                self.selected_label.state = LabelStates.FULL
                if self.selected_label.holder:
                    self.selected_label.holder.label = None
                    self.selected_label.holder = None
                return

    def on_dragging(self):
        if not self.dragging:
            return
        self.selected_label.y -= (self.selected_label.y - Input.mouse.y) / (0.01 / Time.dt)
        self.selected_label.x -= (self.selected_label.x - Input.mouse.x) / (0.01 / Time.dt)

    def end_dragging_class(self):
        if not self.dragging:
            return
        if not self.selected_label:
            return
        if not isinstance(self.selected_label, ClassLabel):
            return
        if Input.mouse.buttons["left_hold"]:
            return

        self.dragging = False

        if not self.class_holder.rect.collidepoint(Input.mouse.position):
            self.selected_label.reposition()
            if self.class_answer == self.selected_label:
                self.clear_holders()
                self.clear_default_labels()
                self.selected_label = None
                self.reposition_answers()
                self.clear_custom_labels()
                self.clear_points()
            return

        # Check swap
        if self.class_answer:
            self.class_answer.reposition()
            self.clear_holders()
            self.clear_default_labels()
            self.reposition_answers()
            self.clear_custom_labels()

        self.class_answer = self.selected_label
        self.class_answer.position = self.class_holder.rect.center
        self.class_answer.state = LabelStates.FULL
        self.set_default_labels()
        self.set_holders()
        self.set_custom_labels()
        self.set_points()
        self.selected_label = None
        self.dragging = False

    def end_dragging_answer(self):
        if not self.dragging:
            return
        if not self.selected_label:
            return
        if not isinstance(self.selected_label, Label):
            return
        if Input.mouse.buttons["left_hold"]:
            return
        answer_holder: None | LabelHolder = None
        for holder in self.holders.sprites():
            holder: LabelHolder
            if holder.rect.collidepoint(Input.mouse.position):
                answer_holder = holder
                break
        if not answer_holder:
            self.selected_label.reposition()
            self.selected_label = None
            self.dragging = False
            return
        if answer_holder.label:
            answer_holder.label.holder = None
            answer_holder.label.reposition()

        answer_holder.label = self.selected_label
        self.selected_label.holder = answer_holder
        self.selected_label.state = LabelStates.FULL
        self.selected_label = None
        self.dragging = False

        if self.data.correctAnswers == self.get_answers():
            self.continue_message.add(self.group)
            self.can_drag = False

    def drag(self):
        # Start dragging
        if not self.dragging and Input.mouse.buttons["left_hold"]:
            for label in self.class_labels.sprites() + self.labels.sprites():
                if label.rect.collidepoint(Input.mouse.position):
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
            self.selected_label.y -= (self.selected_label.y - Input.mouse.y) / (0.01 / Time.dt)
            self.selected_label.x -= (self.selected_label.x - Input.mouse.x) / (0.01 / Time.dt)

        # End dragging
        if self.dragging and not Input.mouse.buttons["left_hold"]:
            if isinstance(self.selected_label, ClassLabel):
                if self.class_holder.rect.collidepoint(Input.mouse.position):
                    # Check swap
                    if self.class_answer:
                        print("Swaping")
                        self.class_answer.position = self.class_positions[self.class_answer.network_class]
                        self.class_answer.state = LabelStates.STICK
                        self.holders = SpriteGroup()
                        for label in self.df_labels.sprites():
                            label: Label
                            label.value = ""

                    self.selected_label.position = self.class_holder.rect.center
                    self.class_answer = self.selected_label
                    default_mask = self.default_masks[self.class_answer.network_class]
                    print(f"Setting class {self.class_answer.network_class}")
                    print(f"Default mask {default_mask}")
                    print(f"Holders {self.holders_number[self.class_answer.network_class]}")

                    for index, number in enumerate(default_mask):
                        self.df_labels.sprites()[index].value = number

                    for index in range(4 - self.holders_number[self.class_answer.network_class]):
                        Label((340 + 25 + (65 * index), 308 + 12.5), 255, True, self.group, self.cm_labels)

                    if not self.holders.sprites():
                        for index in range(self.holders_number[self.class_answer.network_class]):
                            x_padding = (3 - self.holders_number[self.class_answer.network_class]) * 65
                            LabelHolder((400 + x_padding + (index * 65), 301), self.group, self.holders)
                    for index in range(3):
                        Text((340 + 50 + 7.5 + (index * 65), 308 + 13.5), ".", 32, Colors.DARK, self.group, font="fool",
                             shadow=False)

                    if self.class_answer.network_class == self.data.ipClass.lower():
                        self.class_holder.deactivate()
                        self.drag_class = False
                else:
                    self.selected_label.position = self.class_positions[self.selected_label.network_class]
                    self.selected_label.state = LabelStates.STICK

                    if self.selected_label == self.class_answer:
                        self.class_answer = None

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
                    if holder.rect.collidepoint(Input.mouse.position) and holder.active:
                        if holder.label:
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
            if holder.label:
                answers.append(holder.label.value)
            else:
                answers.append("")

        return answers

    def update(self) -> None:
        self.group.update()
        # Tab
        if self.tab.clicked and self.continue_message in self.group.sprites():
            self.scene.set_stage(Zone(self.scene, self.data.zone_id))
        # Get answers
        # class_answer = ""
        # label_answers = []
        # if Input.keyboard.keys["space"]:
        #     print(self.class_answer.network_class)
        #     class_answer = self.class_answer.network_class
        #     for holder in self.holders.sprites():
        #         holder: LabelHolder
        #         for label in self.labels.sprites():
        #             label: Label
        #             if label.holder == holder:
        #                 label_answers.append(str(label.value))
        #     if class_answer == self.data.ipClass.lower() and label_answers == self.data.correctAnswers:
        #         print("good")
        #     else:
        #         print("bad")

        self.start_dragging_class()
        self.start_dragging_answer()
        self.on_dragging()
        self.end_dragging_class()
        self.end_dragging_answer()

    def render(self) -> None:
        self.group.render(self.display)
        if self.selected_label:
            self.selected_label.render(self.display)
