import pygame.mixer

from engine.window import Window
from engine.data import Data
from engine.input import Input
from engine.scene.scene import Stage, StagedScene
from engine.ui.text import Text
from engine.ui.image import Image
from engine.objects.sprite import SpriteGroup
from engine.constants import Colors
from src.scenes.main_menu.main_menu_objects import Option
from src.scenes.main_menu.stage_objects import ExitButton, DeleteButton
from src.scenes.character_creation.character_creation import CharacterCreation
from engine.assets import Assets
import src.scenes.loading.loading as loading
from src.scenes.main_menu.stage_objects import DescriptionTitle
from src.scenes.world.world import World
from engine.audio import AudioManager
from engine.save_manager import instance as save_manager

description_text = "Archivo de guardado de @"
empty_description = "Empezar una nueva aventura en Celestia"


class NewGame(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("new_game", scene)
        self.group = SpriteGroup()
        self.interactive = SpriteGroup()
        self.save_buttons = SpriteGroup()
        Text((251, 80), "JUGAR", 32, Colors.WHITE, self.group, shadow=False)
        Image((51, 54), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 99), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 246), Assets.images_main_menu["doted_line"], self.group, centered=False)
        Image((51, 290), Assets.images_main_menu["doted_line"], self.group, centered=False)
        self.exit_button = ExitButton((110, 69), self.group, self.interactive)
        self.description = Text((250, 268), "", 16, Colors.WHITE, self.group, shadow=False)
        self.description_title = DescriptionTitle((256, 245), "", self.group)
        for index, save in enumerate(save_manager.saves):
            if save.name == "":
                Option("- VACIO -", (96, 119 + (30 * index)), self.group, self.interactive, self.save_buttons)
            else:
                Option(save.name, (96, 119 + (30 * index)), self.group, self.interactive, self.save_buttons)

    def update(self) -> None:
        self.group.update()
        if Input.keyboard.keys["esc"] or self.exit_button.clicked:
            self.scene.exit_stage()

        # Change cursor
        if any([sprite.hovered for sprite in self.interactive.sprites()]):
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

        for index, save_button in enumerate(self.save_buttons.sprites()):
            save_button: Option
            if save_button.hovered:
                if save_button.text.text != "- VACIO -":
                    self.description_title.activate()
                    self.description.activate()
                    players_name = save_manager.saves[index].name
                    time_played = save_manager.saves[index].time
                    self.description_title.text = players_name
                    self.description.text = \
                        description_text[:].replace("@", players_name).replace("tt", str(time_played % 60))
                else:
                    self.description_title.text = "Nuevo Juego"
                    self.description.text = empty_description
            if save_button.clicked:
                self.transitionPosition = save_button.rect.center
                save_manager.active_save = index
                from engine.scene.scene_manager import SceneManager
                if save_button.text.text == "- VACIO -":

                    SceneManager.change_scene(loading.Loading(Assets.load_character_creation_assets,
                                                              CharacterCreation))
                elif not SceneManager.transitioning:
                    AudioManager.play_music("exploration")
                    from src.scenes.world.time_manager import TimeManager
                    TimeManager.current_day_of_week = save_manager.active_save.week_day
                    SceneManager.change_scene(loading.Loading(Data.load_world, World), True)

    def render(self) -> None:
        self.group.render(self.display)
