import src.engine.assets as assets
import src.engine.window as window
import src.engine.input as game_input
import src.scene.core.scene_manager as scene_manager
import src.engine.data as data
import src.user.preferences as preferences
import src.user.saves as saves
from src.scene.core.scene import Stage, StagedScene
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.game_object.sprite import SpriteGroup
from src.constants.colors import *
from src.scene.main_menu.main_menu_objects import Option
from src.scene.main_menu.stage_objects import ArrowButton, TextButton, ExitButton, DescriptionTitle
from src.scene.character_creation.character_creation import CharacterCreation
import src.scene.loading.loading as loading
from src.scene.map.test_map import TestMap


class NewGame(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("new_game", scene)
        self.default_group = SpriteGroup()
        self.interactive = SpriteGroup()
        self.save_buttons = SpriteGroup()
        GUIText("JUGAR", (251, 80), 32, self.default_group, color=WHITE_MOTION, shadow=False)
        GUIImage("top_line", (51, 54), assets.images_main_menu["doted_line"], self.default_group, centered=False)
        GUIImage("bottom_line", (51, 99), assets.images_main_menu["doted_line"], self.default_group, centered=False)
        GUIImage("top_description_line", (51, 246), assets.images_main_menu["doted_line"], self.default_group,
                 centered=False)
        GUIImage("bottom_description_line", (51, 290), assets.images_main_menu["doted_line"], self.default_group,
                 centered=False)
        self.exit_button = ExitButton((110, 69), self.default_group, self.interactive)

        for index, save in enumerate(saves.saves):
            if save["name"] == "":
                Option("- VACIO -", (96, 119 + (30 * index)), self.default_group, self.interactive, self.save_buttons)
            else:
                Option(save["name"], (96, 119 + (30 * index)), self.default_group, self.interactive, self.save_buttons)

    def update(self) -> None:
        self.default_group.update()

        if game_input.keyboard.keys["esc"] or self.exit_button.clicked:
            self.scene.exit_stage()

        for index, save_button in enumerate(self.save_buttons.sprites()):
            if save_button.clicked:
                self.transitionPosition = save_button.rect.center
                data.active_save = index
                if save_button.name == "- VACIO -":
                    scene_manager.change_scene(self.scene,
                                               loading.Loading(assets.load_character_creation_assets,
                                                               CharacterCreation))
                else:
                    scene_manager.change_scene(self, TestMap(), True)

        # Change cursor
        if any([sprite.hovered for sprite in self.interactive.sprites()]):
            if game_input.mouse.buttons["left_hold"]:
                window.set_cursor("grab")
            else:
                window.set_cursor("hand")
        else:
            window.set_cursor("arrow")

    def render(self) -> None:
        self.default_group.render(self.display)
