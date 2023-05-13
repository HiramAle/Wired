import pygame
from engine.assets import Assets
from engine.window import Window
from engine.input import Input
from engine.scene.scene import Stage, StagedScene
from src.scenes.main_menu.main_menu_objects import Option
from src.utils.maths import sin_wave
from engine.objects.sprite import SpriteGroup
from src.scenes.main_menu.options_stage import OptionsStage
from src.scenes.main_menu.play_stage import NewGame
from engine.ui.image import Image


class MainMenuStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("main_menu_stage", scene)
        self.group = SpriteGroup()
        self.logo = Image((251, 130), Assets.images_misc["logo"], self.group)
        self.play = Option("- JUGAR -", (96, 167), self.group)
        self.options = Option("- OPCIONES -", (96, 197), self.group)
        self.exit = Option("- SALIR -", (96, 227), self.group)

    def update(self):
        self.group.update()
        self.logo.y = sin_wave(115, 5, 200)

        if any([option.hovered for option in self.group.sprites() if isinstance(option, Option)]):
            Window.set_cursor("hand")
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
        else:
            Window.set_cursor("arrow")

        if self.play.clicked:
            self.scene.set_stage(NewGame(self.scene))

        if self.options.clicked:
            self.scene.set_stage(OptionsStage(self.scene))

        if self.exit.clicked:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def render(self) -> None:
        self.group.render(self.display)
