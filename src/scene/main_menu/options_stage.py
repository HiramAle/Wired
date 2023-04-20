import src.engine.assets as assets
import src.engine.window as window
import src.engine.input as input
import src.engine.audio as audio
import src.user.preferences as preferences
from src.scene.core.scene import Stage, StagedScene
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.game_object.sprite import SpriteGroup
from src.constants.colors import *
from src.scene.main_menu.stage_objects import ArrowButton, TextButton, ExitButton, DescriptionTitle


def format_size(size: tuple) -> str:
    return f"{size[0]} x {size[1]}"


class OptionsStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("options_stage", scene)
        window.set_cursor("arrow")
        self.descriptions = {"RESOLUCIÓN": "Cambia el tamaño de la ventana del juego.",
                             "VOLÚMEN": "Cambia el volúmen de los efectos y la música.",
                             "GUARDAR": "Guarda las preferencias.",
                             "SALIR": "Regresa al menú principal."}
        self.option = ""
        self.group = SpriteGroup()
        self.interactive = SpriteGroup()
        self.display_group = SpriteGroup()
        self.volume_group = SpriteGroup()
        GUIText("OPCIONES", (209, 61), 32, self.group, color=WHITE_MOTION, centered=False, shadow=False)
        GUIImage("top_line", (51, 54), assets.images_main_menu["doted_line"], self.group, centered=False)
        GUIImage("bottom_line", (51, 99), assets.images_main_menu["doted_line"], self.group, centered=False)
        GUIImage("top_description_line", (51, 246), assets.images_main_menu["doted_line"], self.group, centered=False)
        GUIImage("bottom_description_line", (51, 290), assets.images_main_menu["doted_line"], self.group,
                 centered=False)
        self.description = GUIText(self.descriptions.get("volume"), (250, 268), 16, self.group, shadow=False)
        self.exit_button = ExitButton((110, 69), self.group, self.interactive)
        # Preferences
        self.display_sizes = [(960, 540), (1280, 720), (1920, 1080)]
        self.size_index = self.display_sizes.index((preferences.window_width, preferences.window_height))
        self.selected_size = self.display_sizes[self.size_index]
        # Display
        self.size_text = GUIText(format_size(self.selected_size), (250, 130), 32, self.group, self.display_group,
                                 color=BLUE_MOTION, shadow=False)
        self.display_left = ArrowButton((96 + 70, 130), "right", self.group, self.display_group, self.interactive)
        self.display_right = ArrowButton((96 + 310 - 70, 130), "left", self.group, self.display_group, self.interactive)
        # Volume
        self.volume_left = ArrowButton((96 + 70, 170), "right", self.group, self.volume_group, self.interactive)
        self.volume_right = ArrowButton((96 + 310 - 70, 170), "left", self.group, self.volume_group, self.interactive)
        self.description_title = DescriptionTitle((256, 245), "Pantalla", self.group)
        self.hidden_index = preferences.volume
        self.music_icons: list[GUIImage] = []
        for i in range(5):
            sprite = GUIImage("music", (190 + (i * 30), 170), assets.images_main_menu["note_music"], self.group,
                              self.volume_group)
            if i > preferences.volume:
                if i < self.hidden_index:
                    self.hidden_index = i
                sprite.opacity = 0
            self.music_icons.append(sprite)

        self.apply_button = TextButton("- GUARDAR -", (197, 210), self.group, self.interactive)

    def update(self):
        self.group.update()
        # Change description
        if any([sprite.hovered for sprite in self.display_group.sprites()]):
            self.option = "RESOLUCIÓN"
        elif any([sprite.hovered for sprite in self.volume_group.sprites()]):
            self.option = "VOLÚMEN"
        elif self.apply_button.hovered:
            self.option = "GUARDAR"
        elif self.exit_button.hovered:
            self.option = "SALIR"
        else:
            self.option = ""
        self.description.text = self.descriptions.get(self.option, "")
        self.description_title.text = self.option
        # Return stage
        if input.keyboard.keys["esc"] or self.exit_button.clicked:
            self.scene.exit_stage()
        # Volume changer
        if self.volume_left.clicked:
            if self.hidden_index >= 0:
                self.music_icons[self.hidden_index].opacity = 0
                self.hidden_index -= 1
        if self.volume_right.clicked:
            if self.hidden_index < 4:
                self.hidden_index += 1
                self.music_icons[self.hidden_index].opacity = 255

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
            window.set_window_size(self.selected_size)
            audio.set_volume(self.hidden_index)

        # Change cursor
        if any([sprite.hovered for sprite in self.interactive.sprites()]):
            if input.mouse.buttons["left_hold"]:
                window.set_cursor("grab")
            else:
                window.set_cursor("hand")
        else:
            window.set_cursor("arrow")

    def render(self) -> None:
        self.group.render(self.display)
