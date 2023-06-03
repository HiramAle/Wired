import pygame
from engine.assets import Assets
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, Button


class Exit(Scene):
    def __init__(self):
        super().__init__("exit")
        self.x_padding = 8
        self.exit = SpriteGroup()
        Text((155 + self.x_padding, 42), "Salir", 32, Colors.SPRITE, self.exit, centered=False)
        Text((455.5 + self.x_padding, 76.5 - 20), "Zzzz.", 16, Colors.SPRITE, self.exit)
        Text((455.5 + self.x_padding, 76.5 + 20), "Duerme para guardar tu progreso.", 16, Colors.SPRITE, self.exit)
        Text((456 + self.x_padding, 127),
             "La próxima vez\nque entres,\nretomaras desde\nel ultimo día\nen que hayas\ndormido. ", 16, Colors.SPRITE,
             self.exit, centered=False)
        Sprite((390.5 + self.x_padding, 208), Assets.images_book["bed"], self.exit)
        PlayerAvatar((390.5 + self.x_padding, 208), "sleep", self.exit)
        # self.menu_button = Button((104, 120), "button_menu", self.exit, self.interactive, centered=False)
        self.desktop_button = Button((104, 120), "button_desktop", self.exit, self.interactive, centered=False)
        self.module_button = None
        from engine.scene.scene_manager import SceneManager
        SceneManager.print_stack()
        if SceneManager.stack_scene[-1].name != "world":
            self.module_button = Button((104, 194), "button_module", self.exit, centered=False)

    def update(self) -> None:
        self.exit.update()
        from engine.scene.scene_manager import SceneManager
        # if self.menu_button.clicked:
        #     from src.scenes.main_menu.main_menu import MainMenu
        #     SceneManager.change_scene(MainMenu(), transition=True,empty=True)
        if self.desktop_button.clicked:
            import sys
            sys.exit()
        if self.module_button:
            if self.module_button.clicked:
                from engine.scene.scene_manager import SceneManager
                SceneManager.exit_scene()
                SceneManager.exit_scene()

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.exit.render(self.display)
