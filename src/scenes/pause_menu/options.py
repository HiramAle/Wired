import pygame
from engine.assets import Assets
from engine.audio import AudioManager
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from engine.preferences import Preferences
from src.scenes.pause_menu.pause_objects import PlayerAvatar, Button
from engine.ui.button import Button as Btn
from engine.window import Window


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
        self.volume = Text((188 + self.x_padding, 241), f"{int(Preferences.volume * 100 / 25)}%",
                           32, Colors.SPRITE, self.options)
        Text((403 + self.x_padding, 42), "Controles", 32, Colors.SPRITE, self.options, centered=False)
        Text((470 + self.x_padding, 105), "Moverse", 16, Colors.SPRITE, self.options, centered=False)
        Text((497 + self.x_padding, 171), "Arrastrar", 16, Colors.SPRITE, self.options, centered=False)
        Text((373 + self.x_padding, 171), "Interactuar", 16, Colors.SPRITE, self.options, centered=False)
        Text((388 + self.x_padding, 226), "Inventario", 16, Colors.SPRITE, self.options, centered=False)
        Text((505 + self.x_padding, 226), "Trabajos", 16, Colors.SPRITE, self.options, centered=False)
        Text((377 + self.x_padding, 258), "Mapa", 16, Colors.SPRITE, self.options, centered=False)
        Text((505 + self.x_padding, 258), "Salir", 16, Colors.SPRITE, self.options, centered=False)
        Sprite((407 + self.x_padding, 88), Assets.images_book["key_w"], self.options, centered=False)
        Sprite((383 + self.x_padding, 115), Assets.images_book["key_a"], self.options, centered=False)
        Sprite((407 + self.x_padding, 115), Assets.images_book["key_s"], self.options, centered=False)
        Sprite((431 + self.x_padding, 115), Assets.images_book["key_d"], self.options, centered=False)
        Sprite((345 + self.x_padding, 167), Assets.images_book["key_e"], self.options, centered=False)
        Sprite((466 + self.x_padding, 166), Assets.images_book["key_mouse"], self.options, centered=False)
        Sprite((345 + self.x_padding, 219), Assets.images_book["key_esc"], self.options, centered=False)
        Sprite((466 + self.x_padding, 219), Assets.images_book["key_j"], self.options, centered=False)
        Sprite((345 + self.x_padding, 253), Assets.images_book["key_m"], self.options, centered=False)
        Sprite((466 + self.x_padding, 253), Assets.images_book["key_esc"], self.options, centered=False)

        self.size_left = Btn((110, 145), Assets.images_book["button_left_normal"],
                             Assets.images_book["button_left_pressed"], centered=False, outline=False)
        self.size_right = Btn((266, 145), Assets.images_book["button_right_normal"],
                              Assets.images_book["button_right_pressed"], centered=False, outline=False)
        self.sound_left = Btn((110, 235), Assets.images_book["button_left_normal"],
                              Assets.images_book["button_left_pressed"], centered=False, outline=False)
        self.sound_right = Btn((266, 235), Assets.images_book["button_right_normal"],
                               Assets.images_book["button_right_pressed"], centered=False, outline=False)
        self.display_sizes = [(960, 540), (1280, 720), (1920, 1080)]
        if tuple(Preferences.native_resolution) not in self.display_sizes:
            self.display_sizes.append(tuple(Preferences.native_resolution))
        self.size_index = self.display_sizes.index((Preferences.window_width, Preferences.window_height))
        self.selected_size = self.display_sizes[self.size_index]
        self.volume_int = Preferences.volume
        print(f"Preferences volume {self.volume_int}")

    @staticmethod
    def format_size(size: tuple) -> str:
        return f"{size[0]} x {size[1]}"

    def format_volume(self) -> str:
        return f"{int(self.volume_int * 100 / 5)}%"

    def update(self):
        self.size_left.update()
        self.size_right.update()
        self.sound_left.update()
        self.sound_right.update()
        if self.size_left.clicked:
            self.size_index -= 1
            if self.size_index < 0:
                self.size_index = len(self.display_sizes) - 1
            self.selected_size = self.display_sizes[self.size_index]
            Window.set_window_size(self.selected_size)
        if self.size_right.clicked:
            self.size_index += 1
            if self.size_index >= len(self.display_sizes):
                self.size_index = 0
            self.selected_size = self.display_sizes[self.size_index]
            Window.set_window_size(self.selected_size)
        self.resolution.text = self.format_size(self.selected_size)
        if self.sound_left.clicked:
            self.volume_int -= 1
            if self.volume_int < 0:
                self.volume_int = 0
            AudioManager.set_volume(self.volume_int)
        if self.sound_right.clicked:
            self.volume_int += 1
            if self.volume_int > 5:
                self.volume_int = 5
            AudioManager.set_volume(self.volume_int)
        self.volume.text = self.format_volume()

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.options.render(self.display)
        self.size_left.render(self.display)
        self.size_right.render(self.display)
        self.sound_left.render(self.display)
        self.sound_right.render(self.display)
