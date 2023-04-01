import src.engine.assets as assets
from src.scene.core.scene import Stage, StagedScene
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.scene.main_menu.main_menu_objects import Option
from src.utils.maths import sin_wave
from src.game_object.sprite import SpriteGroup
from src.constants.colors import *


class MainMenuStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("main_menu_stage", scene)
        self.logo = GUIImage("logo", (251, 130), assets.images_misc["logo"], self.group)
        self.newGame = Option("- NEW GAME -", (96, 167), self.group)
        self.continueGame = Option("- CONTINUE -", (96, 197), self.group)
        self.options = Option("- OPTIONS -", (96, 227), self.group)
        self.exit = Option("- EXIT -", (96, 257), self.group)

    def update(self):
        super().update()
        self.logo.y = sin_wave(115, 5, 200)
        if self.options.clicked:
            self.scene.set_stage(OptionsStage(self.scene))

        # print(self.group.sprites())


class OptionsStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("options_stage", scene)
        self.group = SpriteGroup()
        GUIText("OPTIONS", (209, 61), 32, self.group, color=WHITE_MOTION, centered=False)
        GUIImage("top_line", (51, 54), assets.images_main_menu["doted_line"], self.group, centered=False)
        GUIImage("bottom_line", (51, 99), assets.images_main_menu["doted_line"], self.group, centered=False)
