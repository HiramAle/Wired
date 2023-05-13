from engine.assets import Assets
from engine.window import Window
from engine.audio import AudioManager
from engine.input import Input
from engine.preferences import Preferences
from engine.scene.scene import Stage, StagedScene
from engine.ui.image import Image
from engine.ui.text import Text
from engine.objects.sprite import SpriteGroup
from engine.constants import Colors
from src.scenes.main_menu.stage_objects import ArrowButton, TextButton, ExitButton, DescriptionTitle


def format_size(size: tuple) -> str:
    return f"{size[0]} x {size[1]}"


class OptionsStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("options_stage", scene)
        Window.set_cursor("arrow")
        self.descriptions = {"RESOLUCIÓN": "Cambia el tamaño de la ventana del juego.",
                             "VOLÚMEN": "Cambia el volúmen de los efectos y la música.",
                             "APLICAR": "Guarda las preferencias.",
                             "SALIR": "Regresa al menú principal."}
        self.option = ""
        self.group = SpriteGroup()
        self.interactive = SpriteGroup()
        self.display_group = SpriteGroup()
        self.volume_group = SpriteGroup()
        Text((209, 61), "OPCIONES", 32, Colors.WHITE, self.group, centered=False, shadow=False)
        # Lines
        Image((51, 54), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 99), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 246), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 290), Assets.images_main_menu["doted_line"], self.group, centered=False)
        self.description = Text((250, 268), self.descriptions.get("volume"), 16, Colors.WHITE, self.group, shadow=False)
        self.exit_button = ExitButton((110, 69), self.group, self.interactive)
        # Preferences
        self.display_sizes = [(960, 540), (1280, 720), (1920, 1080)]
        self.size_index = self.display_sizes.index((Preferences.window_width, Preferences.window_height))
        self.selected_size = self.display_sizes[self.size_index]
        # Display
        self.size_text = Text((250, 130), format_size(self.selected_size), 32, Colors.BLUE, self.group,
                              self.display_group, shadow=False)
        self.display_left = ArrowButton((96 + 70, 130), "right", self.group, self.display_group, self.interactive)
        self.display_right = ArrowButton((96 + 310 - 70, 130), "left", self.group, self.display_group, self.interactive)
        # Volume
        self.volume_left = ArrowButton((96 + 70, 170), "right", self.group, self.volume_group, self.interactive)
        self.volume_right = ArrowButton((96 + 310 - 70, 170), "left", self.group, self.volume_group, self.interactive)
        self.description_title = DescriptionTitle((256, 245), "Pantalla", self.group)
        self.hidden_index = (Preferences.volume // 5) - 1
        self.music_icons: list[Image] = []
        for i in range(5):
            sprite = Image((190 + (i * 30), 170), Assets.images_main_menu["note_music"], self.group, self.volume_group)
            if i > self.hidden_index:
                sprite.deactivate()
            self.music_icons.append(sprite)

        self.apply_button = TextButton("- APLICAR -", (197, 210), self.group, self.interactive)

    def update(self):
        self.group.update()
        # Change description
        if any([sprite.hovered for sprite in self.display_group.sprites()]):
            self.option = "RESOLUCIÓN"
        elif any([sprite.hovered for sprite in self.volume_group.sprites()]):
            self.option = "VOLÚMEN"
        elif self.apply_button.hovered:
            self.option = "APLICAR"
        elif self.exit_button.hovered:
            self.option = "SALIR"
        else:
            self.option = ""
        self.description.text = self.descriptions.get(self.option, "")
        self.description_title.text = self.option
        # Return stage
        if Input.keyboard.keys["esc"] or self.exit_button.clicked:
            self.scene.exit_stage()
        # Volume changer
        if self.volume_left.clicked:
            if self.hidden_index >= 0:
                self.music_icons[self.hidden_index].deactivate()
                self.hidden_index -= 1
        if self.volume_right.clicked:
            if self.hidden_index < 4:
                self.hidden_index += 1
                self.music_icons[self.hidden_index].activate()

        # Display changer
        if self.display_left.clicked:
            self.size_index -= 1
            if self.size_index < 0:
                self.size_index = len(self.display_sizes) - 1
            self.selected_size = self.display_sizes[self.size_index]
        if self.display_right.clicked:
            self.size_index += 1
            if self.size_index >= len(self.display_sizes):
                self.size_index = 0
            self.selected_size = self.display_sizes[self.size_index]
        self.size_text.text = format_size(self.selected_size)
        # Apply button
        if self.apply_button.clicked:
            Window.set_window_size(self.selected_size)
            AudioManager.set_volume((self.hidden_index + 1))

        # Change cursor
        if any([sprite.hovered for sprite in self.interactive.sprites()]):
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

    def render(self) -> None:
        self.group.render(self.display)
