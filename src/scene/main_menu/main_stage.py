import pygame
import src.engine.assets as assets
import src.engine.window as window
import src.engine.input as input
from src.scene.core.scene import Stage, StagedScene
from src.gui.image import GUIImage
from src.scene.main_menu.main_menu_objects import Option
from src.utils.maths import sin_wave
from src.game_object.sprite import SpriteGroup
from src.scene.main_menu.options_stage import OptionsStage


class MainMenuStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("main_menu_stage", scene)
        self.group = SpriteGroup()
        self.logo = GUIImage("logo", (251, 130), assets.images_misc["logo"], self.group)
        self.newGame = Option("- NEW GAME -", (96, 167), self.group)
        self.continueGame = Option("- CONTINUE -", (96, 197), self.group)
        self.options = Option("- OPTIONS -", (96, 227), self.group)
        self.exit = Option("- EXIT -", (96, 257), self.group)

    def update(self):
        self.group.update()
        self.logo.y = sin_wave(115, 5, 200)

        if any([option.hovered for option in self.group.sprites() if isinstance(option, Option)]):
            window.set_cursor("hand")
            if input.mouse.buttons["left_hold"]:
                window.set_cursor("grab")
        else:
            window.set_cursor("arrow")

        if self.options.clicked:
            self.scene.set_stage(OptionsStage(self.scene))

        if self.exit.clicked:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def render(self) -> None:
        self.group.render(self.display)


def format_size(size: tuple) -> str:
    return f"{size[0]} x {size[1]}"
