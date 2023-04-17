import src.engine.time as game_time
from src.scene.core.scene import Stage, StagedScene
from src.game_object.sprite import SpriteGroup
from src.gui.image import GUIImage
from src.scene.subnetting.subnetting_objects import *
from random import shuffle


class Zone(Stage):
    def __init__(self, scene: StagedScene, data: CustomMaskProblem):
        super().__init__("subnet_mask", scene)
        self.data = data
        self.group = SpriteGroup()
        self.labels = SpriteGroup()
        self.buildings = SpriteGroup()
        self.default_labels = SpriteGroup()
        self.holders = SpriteGroup()
        self.selected_building: Building | None = None

        self.answer_positions = [(383, 50), (450, 56), (517, 48), (372, 93), (450, 105), (528, 93), (366, 140),
                                 (443, 151), (517, 139), (379, 186), (450, 196), (523, 185)]
        self.current_subnet_index = 0
        correct_answers = self.data.subnet_answers(self.current_subnet_index)
        self.possible_answers = [randint(0, 255) for index in
                                 range(self.data.ip.split(".").count("0") * 2)] + correct_answers

        shuffle(self.possible_answers)

        tab_image = pygame.Surface((19, 54), pygame.SRCALPHA)
        self.tab = GUIImage("tab", (606, 19), tab_image, centered=False)

        GUIImage("tab", (0, 0), assets.images_subnetting["zone_tab"], self.group, centered=False)
        GUIImage("underscore", (47, 181), assets.images_subnetting["underscore_yellow"], self.group, centered=False)
        GUIImage("underscore", (210, 180), assets.images_subnetting["undescoreyellow"], self.group, centered=False)
        GUIImage("dotted_line", (357, 25.25), assets.images_subnetting["dotted_line"], self.group, centered=False)
        underscore_name = assets.images_subnetting["name_underscore"].copy()
        underscore_name.fill("#FDFFEA")
        underscore_name.blit(assets.images_subnetting["name_underscore"], (0, 0))
        GUIImage("zone_underscore", (435, 17), underscore_name, self.group, centered=False)
        self.posit_it = GUIImage("post_it", (366, 93), assets.images_subnetting["post_it_class"], self.group,
                                 centered=False, scale=2)

        GUIText("Dirección IP:", (45, 188), 32, self.group, font="fool", centered=False, color="#2E2E2E", shadow=False)
        GUIText(self.data.zone, (473.5, 25.5), 16, self.group, font="fool", color="#2E2E2E", shadow=False)
        GUIText(self.data.ip, (276.5, 203), 32, self.group, font="fool", color="#2E2E2E", shadow=False)
        self.building_name = GUIText("", (112, 338.5), 16, font="fool", color="#2E2E2E", shadow=False)

        self.group.add(*self.data.buildings)
        self.buildings.add(*self.data.buildings)

        self.selected_label: Label | None = None
        self.dragging = False

    def drag(self):
        # Start dragging
        if not self.dragging and game_input.mouse.buttons["left_hold"]:
            for label in self.labels.sprites():
                if label.rect.collidepoint(game_input.mouse.position):
                    self.dragging = True
                    self.selected_label = label
                    self.selected_label.state = LabelStates.FULL
                    self.selected_label.layer = 2
                    label.holder = None
                    break

        # On dragging
        if self.dragging:
            self.selected_label.y -= (self.selected_label.y - game_input.mouse.y) / (0.01 / game_time.dt)
            self.selected_label.x -= (self.selected_label.x - game_input.mouse.x) / (0.01 / game_time.dt)

        # End dragging
        if self.dragging and not game_input.mouse.buttons["left_hold"]:
            for holder in self.holders.sprites():
                holder: LabelHolder
                if holder.rect.collidepoint(game_input.mouse.position):
                    self.selected_label.holder = holder
            if not self.selected_label.holder:
                self.selected_label.position = self.selected_label.default_position
                self.selected_label.state = LabelStates.STICK
            self.selected_label.layer = 1
            self.dragging = False

            self.selected_label = None

    def update(self) -> None:
        self.group.update()
        self.labels.update()
        if self.tab.clicked:
            self.scene.exit_stage()

        self.drag()

        if self.selected_building and self.posit_it:
            self.posit_it.kill()
            self.posit_it = None
            GUIImage("building", (96, 272), assets.images_subnetting["test_house"], self.group, scale=2)
            GUIImage("building_indicator", (72, 325), assets.images_subnetting["indicator"], self.group, centered=False)
            self.building_name.add(self.group)
            GUIImage("zone_answers", (360, 42), assets.images_subnetting["zone_answers"], self.group,
                     centered=False)
            GUIText("ID de red:", (182, 253), 32, self.group, centered=False, shadow=False, color=DARK_BLACK_MOTION)
            GUIText("Broadcast", (177, 295), 32, self.group, centered=False, shadow=False, color=DARK_BLACK_MOTION)

            default_labels_number = 4 - self.data.ip.split(".").count("0")
            for index in range(default_labels_number):
                id_label = Label((313 + 25 + (index * 73), 249 + 13.5), int(self.data.ip.split(".")[index]), False,
                                 self.group, self.default_labels)
                broadcast_label = Label((313 + 25 + (index * 73), 297 + 13.5), int(self.data.ip.split(".")[index]),
                                        False, self.group, self.default_labels)
                id_label.state = LabelStates.FULL
                broadcast_label.state = LabelStates.FULL

            for index in range(3):
                GUIText(".", (370 + 6 + (index * 73), 246 + 13.5), 32, self.group, font="fool",
                        shadow=False, color=DARK_BLACK_MOTION)
                GUIText(".", (370 + 6 + (index * 73), 292 + 13.5), 32, self.group, font="fool",
                        shadow=False, color=DARK_BLACK_MOTION)

            for index in range(self.data.ip.split(".").count("0")):
                x_padding = (3 - self.data.ip.split(".").count("0")) * 73
                LabelHolder((382 + x_padding + (index * 73), 246), self.group, self.holders)
                LabelHolder((382 + x_padding + (index * 73), 292), self.group, self.holders)

        changed_selection = False
        for building in self.buildings.sprites():
            building: Building
            if building.clicked:
                if building == self.selected_building:
                    continue
                building.selected = True
                if self.selected_building:
                    self.selected_building.selected = False
                self.selected_building = building
                self.building_name.text = self.selected_building.building_type
                changed_selection = True

        if changed_selection:
            for index, position in enumerate(self.answer_positions):
                Label((position[0] + 27, position[1] + 14.5), self.possible_answers[index], False, self.group,
                      self.labels, layer=1)

    def render(self) -> None:
        self.group.render(self.display)
