from engine.window import Window
from engine.data import Data
from engine.input import Input

from engine.scene.scene import Stage, StagedScene

from engine.ui.text import Text
from engine.ui.image import Image
from engine.objects.sprite import SpriteGroup
from src.constants.colors import *
from src.scenes.main_menu.main_menu_objects import Option
from src.scenes.main_menu.stage_objects import ExitButton
from src.scenes.character_creation.character_creation import CharacterCreation
from engine.assets import Assets
import src.scenes.loading.loading as loading
from src.utils.json_saver import instance as save_manager
from src.scenes.world.world import World


class NewGame(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("new_game", scene)
        self.group = SpriteGroup()
        self.interactive = SpriteGroup()
        self.save_buttons = SpriteGroup()
        Text((251, 80), "JUGAR", 32, WHITE_MOTION, self.group, shadow=False)
        Image((51, 54), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 99), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 246), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 290), Assets.images_main_menu["doted_line"], self.group, centered=False)
        self.exit_button = ExitButton((110, 69), self.group, self.interactive)

        for index, save in enumerate(save_manager.saves):
            if save.name == "":
                Option("- VACIO -", (96, 119 + (30 * index)), self.group, self.interactive, self.save_buttons)
            else:
                Option(save.name, (96, 119 + (30 * index)), self.group, self.interactive, self.save_buttons)

    def update(self) -> None:
        self.group.update()

        if Input.keyboard.keys["esc"] or self.exit_button.clicked:
            self.scene.exit_stage()

        for index, save_button in enumerate(self.save_buttons.sprites()):
            if save_button.clicked:
                self.transitionPosition = save_button.rect.center
                save_manager.index = index
                if save_button.name == "- VACIO -":
                    from engine.scene.scene_manager import SceneManager
                    SceneManager.change_scene(self.scene,
                                              loading.Loading(Assets.load_character_creation_assets,
                                                              CharacterCreation))
                else:
                    print("a")
                    # scene_manager.change_scene(self.scene, loading.Loading(Data.load_maps, World), True)
                    # scene_manager.change_scene(self.scenes, loading.Loading(data.load_map, TestMap, ("playershouse",),
                    #                                                        ("playershouse",)), True)

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
