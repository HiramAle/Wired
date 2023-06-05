from engine.scene.scene import Stage, StagedScene
from engine.objects.sprite import SpriteGroup
from engine.ui.image import Image
from src.scenes.subnetting.subnetting_objects import *
from random import shuffle
from engine.assets import Assets
from engine.ui.text import Text
from engine.data import Data


class Zone(Stage):
    def __init__(self, scene: StagedScene, zone_id: str):
        super().__init__("zone_stage", scene)
        self.data = Data.subnetting[zone_id]
        self.group = SpriteGroup()
        self.labels = SpriteGroup()
        self.buildings = SpriteGroup()
        self.default_labels = SpriteGroup()
        self.holders = SpriteGroup()
        self.selected_building: Building | None = None

        self.answer_positions = [(383, 50), (450, 56), (517, 48), (372, 93), (450, 105), (528, 93), (366, 140),
                                 (443, 151), (517, 139), (379, 186), (450, 196), (523, 185)]
        self.subnet_index = 0
        self.correct_answers = self.data.subnet_answers(self.subnet_index)
        other_answers = [randint(0, 255) for index in range(12 - len(self.correct_answers))]
        self.possible_answers = self.correct_answers + other_answers
        shuffle(self.possible_answers)

        tab_image = pygame.Surface((19, 54), pygame.SRCALPHA)
        self.tab = Image((606, 19), tab_image, centered=False)
        self.finished = False

        Image((0, 0), Assets.images_subnetting["zone_tab"], self.group, centered=False)
        Image((47, 181), Assets.images_subnetting["underscore_yellow"], self.group, centered=False)
        Image((210, 180), Assets.images_subnetting["undescoreyellow"], self.group, centered=False)
        Image((357, 25.25), Assets.images_subnetting["dotted_line"], self.group, centered=False)
        underscore_name = Assets.images_subnetting["name_underscore"].copy()
        underscore_name.fill("#FDFFEA")
        underscore_name.blit(Assets.images_subnetting["name_underscore"], (0, 0))
        Image((435, 17), underscore_name, self.group, centered=False)
        self.posit_it = Image((366, 93), Assets.images_subnetting["post_it_class"], self.group, centered=False, scale=2)
        self.instructions = Text((483, 170), "Selecciona en\nel mapa una\nárea para\nconfigurar.", 32, Colors.SPRITE,
                                 self.group)
        self.alert = Text((483, 240), "El proceso es por\nsubneteo tradicional.", 16, Colors.SPRITE, self.group)
        Text((45, 188), "Dirección IP:", 32, "#2E2E2E", self.group, font="fool", centered=False, shadow=False)
        Text((473.5, 25.5), self.data.zone_name, 16, "#2E2E2E", self.group, font="fool", shadow=False)
        Text((276.5, 203), self.data.ip, 32, "#2E2E2E", self.group, font="fool", shadow=False)
        self.building_name = Text((112, 338.5), "", 16, "#2E2E2E", font="fool", shadow=False)
        self.continue_message = Text((369.5, 339.5), "Selecciona un lugar en el mapa para configurar", 16, "#2E2E2E",
                                     shadow=False)

        self.group.add(*self.data.buildings)
        self.buildings.add(*self.data.buildings)

        self.selected_label: Label | None = None
        self.dragging = False
        self.finished_subnet = True
        self.can_drag = True

    def start_dragging(self):
        if not self.can_drag:
            return
        # If is dragging, cant start dragging
        if self.dragging:
            return
        # If it is not dragging but player doesn't press left hold, cant start dragging
        if not Input.mouse.buttons["left_hold"]:
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

    def en_dragging(self):
        if not self.dragging:
            return
        if not self.selected_label:
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

        print(f"Answers are correct? {self.correct_answers} = {self.get_answers()}")
        if self.correct_answers == self.get_answers():
            self.continue_message.add(self.group)
            self.selected_building.done = True
            self.selected_building.subnet = self.data.subnets[self.subnet_index]
            self.continue_message.add(self.group)
            self.finished_subnet = True
            self.subnet_index += 1
            self.can_drag = False
            if self.subnet_index == self.data.subnetsNeeded:
                print("finished")
                self.finished = True

    def drag(self):
        # Start dragging
        if not self.dragging and Input.mouse.buttons["left_hold"]:
            for label in self.labels.sprites():
                if label.rect.collidepoint(Input.mouse.position):
                    self.dragging = True
                    self.selected_label = label
                    self.selected_label.state = LabelStates.FULL
                    self.selected_label.layer = 2
                    label.holder = None
                    break

        # On dragging
        if self.dragging:
            self.selected_label.y -= (self.selected_label.y - Input.mouse.y) / (0.01 / Time.dt)
            self.selected_label.x -= (self.selected_label.x - Input.mouse.x) / (0.01 / Time.dt)

        # End dragging
        if self.dragging and not Input.mouse.buttons["left_hold"]:
            for holder in self.holders.sprites():
                holder: LabelHolder
                if holder.rect.collidepoint(Input.mouse.position):
                    self.selected_label.holder = holder
            if not self.selected_label.holder:
                self.selected_label.position = self.selected_label.default_position
                self.selected_label.state = LabelStates.STICK

            self.selected_label.layer = 1
            self.dragging = False
            self.selected_label = None

            used_holders = len([label.holder for label in self.labels.sprites() if label.holder])

            if self.data.blanks * 2 == used_holders:
                print(f"{self.correct_answers} == {self.get_answers()}?")
                if self.correct_answers == self.get_answers():
                    self.selected_building.subnet = self.data.subnets[self.subnet_index]
                    self.continue_message.add(self.group)
                    self.finished_subnet = True
                    self.subnet_index += 1

                    if self.subnet_index == self.data.subnetsNeeded:
                        print("finished")
                        self.finished = True

    def generate_answers(self):
        if self.subnet_index == self.data.subnetsNeeded:
            return
        print("Generating new answers")
        self.correct_answers = self.data.subnet_answers(self.subnet_index)
        other_answers = [randint(0, 255) for index in range(12 - len(self.correct_answers))]
        self.possible_answers = self.correct_answers + other_answers
        shuffle(self.possible_answers)

        for label in self.labels.sprites():
            label.kill()

        for index, position in enumerate(self.answer_positions):
            Label((position[0] + 27, position[1] + 14.5), self.possible_answers[index], False, self.group,
                  self.labels, layer=1)
        print(self.possible_answers)

    def get_answers(self):
        answers = []
        for holder in self.holders.sprites():
            holder: LabelHolder
            for label in self.labels.sprites():
                label: Label
                if label.holder == holder:
                    answers.append(label.value)
        id_answer = []
        broadcast_answer = []
        for index, answer in enumerate(answers):
            if index % 2 != 0:
                id_answer.append(str(answer))
            else:
                broadcast_answer.append(str(answer))
        return [*broadcast_answer, *id_answer]

    def update(self) -> None:
        self.group.update()
        self.labels.update()

        # self.drag()
        self.start_dragging()
        self.on_dragging()
        self.en_dragging()

        if self.selected_building and self.posit_it:
            self.posit_it.kill()
            self.instructions.kill()
            self.alert.kill()
            self.posit_it = None
            Image((96, 272), Assets.images_subnetting["test_house"], self.group, scale=2)
            Image((72, 325), Assets.images_subnetting["indicator"], self.group, centered=False)
            self.building_name.add(self.group)
            Image((360, 42), Assets.images_subnetting["zone_answers"], self.group,
                  centered=False)
            Text((182, 253), "ID de red:", 32, Colors.DARK, self.group, centered=False, shadow=False)
            Text((177, 295), "Broadcast", 32, Colors.DARK, self.group, centered=False, shadow=False)

            default_labels_number = 4 - self.data.ip.split(".").count("0")
            for index in range(default_labels_number):
                id_label = Label((313 + 25 + (index * 73), 249 + 13.5), int(self.data.ip.split(".")[index]), False,
                                 self.group, self.default_labels)
                broadcast_label = Label((313 + 25 + (index * 73), 297 + 13.5), int(self.data.ip.split(".")[index]),
                                        False, self.group, self.default_labels)
                id_label.state = LabelStates.FULL
                broadcast_label.state = LabelStates.FULL

            for index in range(3):
                Text((370 + 6 + (index * 73), 246 + 13.5), ".", 32, Colors.DARK, self.group, font="fool", shadow=False)
                Text((370 + 6 + (index * 73), 292 + 13.5), ".", 32, Colors.DARK, self.group, font="fool", shadow=False)

            for index in range(self.data.ip.split(".").count("0")):
                x_padding = (3 - self.data.ip.split(".").count("0")) * 73
                LabelHolder((382 + x_padding + (index * 73), 246), self.group, self.holders)
                LabelHolder((382 + x_padding + (index * 73), 292), self.group, self.holders)

        changed_selection = False
        for building in self.buildings.sprites():
            building: Building
            if building.clicked and self.finished_subnet:
                # if building == self.selected_building:
                #     continue
                if building.done:
                    break
                building.selected = True
                self.can_drag = True
                if self.selected_building:
                    self.selected_building.selected = False
                self.selected_building = building
                self.building_name.text = self.selected_building.building_type
                changed_selection = True
                self.finished_subnet = False

        if changed_selection:
            if self.continue_message in self.group.sprites():
                self.continue_message.remove(self.group)
            self.generate_answers()

        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            from src.scenes.pause_menu.pause import Pause
            SceneManager.change_scene(Pause())

        if Input.keyboard.keys["backspace"]:
            pygame.image.save(self.display, "screen_shoot.png")

    def render(self) -> None:
        self.group.render(self.display)
        if self.selected_label:
            self.selected_label.render(self.display)
