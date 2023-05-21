import pygame
from engine.assets import Assets
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from engine.preferences import Preferences
from src.scenes.pause_menu.pause_objects import PlayerAvatar, Button


class Options(Scene):
    def __init__(self):
        super().__init__("options")
        self.x_padding = 8
        self.options = SpriteGroup()
        Text((140 + self.x_padding, 42), "Opciones", 32, Colors.SPRITE, self.options, centered=False)
        Text((128 + self.x_padding, 105), "Resolución", 32, Colors.SPRITE, self.options, centered=False)
        self.resolution = Text((188 + self.x_padding, 152), f"{Preferences.window_width} x {Preferences.window_height}",
                               32, Colors.SPRITE, self.options)
        Text((146 + self.x_padding, 199), "Volúmen", 32, Colors.SPRITE, self.options, centered=False)
        self.volume = Text((188 + self.x_padding, 241), f"{int(Preferences.volume * 100 / 20)}%",
                           32, Colors.SPRITE, self.options)
        Text((403 + self.x_padding, 42), "Controles", 32, Colors.SPRITE, self.options, centered=False)
        Text((470 + self.x_padding, 105), "Moverse", 16, Colors.SPRITE, self.options, centered=False)
        Text((497 + self.x_padding, 171), "Arrastrar", 16, Colors.SPRITE, self.options, centered=False)
        Text((373 + self.x_padding, 171), "Interactuar", 16, Colors.SPRITE, self.options, centered=False)
        Text((388 + self.x_padding, 226), "Inventario", 16, Colors.SPRITE, self.options, centered=False)
        Text((505 + self.x_padding, 226), "Opciones", 16, Colors.SPRITE, self.options, centered=False)
        Text((377 + self.x_padding, 258), "Glosario", 16, Colors.SPRITE, self.options, centered=False)
        Text((505 + self.x_padding, 258), "Salir", 16, Colors.SPRITE, self.options, centered=False)
        Sprite((407 + self.x_padding, 88), Assets.images_book["key_w"], self.options, centered=False)
        Sprite((383 + self.x_padding, 115), Assets.images_book["key_a"], self.options, centered=False)
        Sprite((407 + self.x_padding, 115), Assets.images_book["key_s"], self.options, centered=False)
        Sprite((431 + self.x_padding, 115), Assets.images_book["key_d"], self.options, centered=False)
        Sprite((345 + self.x_padding, 167), Assets.images_book["key_e"], self.options, centered=False)
        Sprite((466 + self.x_padding, 166), Assets.images_book["key_mouse"], self.options, centered=False)
        Sprite((345 + self.x_padding, 219), Assets.images_book["key_tab"], self.options, centered=False)
        Sprite((466 + self.x_padding, 219), Assets.images_book["key_o"], self.options, centered=False)
        Sprite((345 + self.x_padding, 253), Assets.images_book["key_g"], self.options, centered=False)
        Sprite((466 + self.x_padding, 253), Assets.images_book["key_esc"], self.options, centered=False)

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.options.render(self.display)
