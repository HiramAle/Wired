import math
import pygame
from engine.assets import Assets
from engine.input import Input
from engine.data import Data
from engine.save_manager import SaveManager
from engine.window import Window

from engine.scene.scene import Scene
from engine.objects.sprite import SpriteGroup
from engine.ui.image import Image
from engine.ui.text import Text
from src.scenes.character_creation.avatar import Avatar
from src.scenes.character_creation.colors import ColorPicker
from src.constants.colors import *
from src.scenes.character_creation.character_objects import Tab, NameLabel
from engine.save_manager import instance as save_manager
from src.scenes.loading.loading import Loading
from src.scenes.world.world import World
from engine.constants import Colors
from engine.audio import AudioManager
from engine.playerdata import PlayerData

alphabet_dict = {
    'a': [(1, 5), (3, 1), (5, 5), (3, 8), (1, 5), (5, 5)],
    'b': [(1, 1), (1, 8), (3, 8), (4, 7), (4, 5), (3, 4), (1, 4), (3, 4), (4, 3), (4, 1), (3, 1), (1, 1)],
    'c': [(5, 5), (3, 1), (1, 1), (1, 8), (3, 8)],
    'd': [(1, 1), (1, 8), (3, 8), (5, 6), (5, 3), (3, 1), (1, 1)],
    'e': [(5, 1), (1, 1), (1, 4), (3, 4), (1, 4), (1, 8), (5, 8)],
    'f': [(1, 1), (1, 4), (3, 4), (1, 4), (1, 8), (5, 8)],
    'g': [(5, 5), (3, 1), (1, 1), (1, 8), (3, 8), (5, 6), (3, 6)],
    'h': [(1, 1), (1, 8), (1, 5), (5, 5), (5, 1), (5, 8)],
    'i': [(3, 1), (3, 8)],
    'j': [(3, 1), (3, 8), (2, 8), (1, 7), (1, 5)],
    'k': [(1, 1), (1, 8), (1, 5), (4, 8), (5, 8), (2, 4), (5, 1), (4, 1), (1, 4)],
    'l': [(1, 1), (1, 8), (3, 8)],
    'm': [(1, 8), (1, 1), (3, 4), (5, 1), (5, 8)],
    'n': [(1, 1), (1, 8), (5, 1), (5, 8)],
    'o': [(1, 1), (1, 8), (5, 8), (5, 1), (1, 1)],
    'p': [(1, 1), (1, 8), (3, 8), (5, 6), (3, 6), (1, 4)],
    'q': [(1, 1), (1, 8), (3, 8), (5, 6), (5, 4), (3, 4), (5, 4), (5, 1), (1, 1)],
    'r': [(1, 1), (1, 8), (3, 8), (4, 7), (4, 5), (3, 4), (1, 4), (3, 4), (4, 3), (4, 1), (3, 1)],
    's': [(5, 1), (1, 1), (1, 4), (5, 4), (5, 5), (1, 5), (1, 8), (5, 8)],
    't': [(1, 1), (5, 1), (3, 1), (3, 8)],
    'u': [(1, 1), (1, 8), (3, 8), (5, 1), (5, 8)],
    'v': [(1, 1), (3, 8), (5, 1)],
    'w': [(1, 1), (1, 8), (3, 5), (5, 8), (5, 1)],
    'x': [(1, 1), (5, 8), (3, 5), (5, 1), (1, 8)],
    'y': [(1, 1), (3, 4), (3, 8), (3, 4), (5, 1)],
    'z': [(1, 1), (5, 1), (1, 8), (5, 8)]}


class CharacterCreation(Scene):
    def __init__(self):
        super().__init__("character_creation")
        pygame.mouse.set_visible(True)
        self.default_group = SpriteGroup()
        self.character_selection = SpriteGroup()
        self.character_info = SpriteGroup()
        self.interactive = SpriteGroup()
        Image((0, 0), Assets.images_character_creation["players_house_background"], self.default_group,
              centered=False)
        self.clipboard = Image((21, 31), Assets.images_character_creation["clip_board"], self.default_group,
                               centered=False)
        self.avatar = Avatar(self.default_group)
        table_image = pygame.Surface((274, 309), pygame.SRCALPHA)
        table_image.fill((122, 73, 76, 48))
        self.clipboard_padding = self.clipboard.rect.centerx + 3
        Text((self.clipboard_padding, 94), "Piel", 32, Colors.SPRITE, self.character_selection, shadow=False)
        Text((self.clipboard_padding, 150), "Ojos", 32, Colors.SPRITE, self.character_selection, shadow=False)
        Text((self.clipboard_padding, 206), "Color de cabello", 32, Colors.SPRITE, self.character_selection,
             shadow=False)
        Text((self.clipboard_padding, 262), "Color de ropa", 32, Colors.SPRITE, self.character_selection,
             shadow=False)

        self.skin_picker = ColorPicker((self.clipboard_padding, 122), Data.body_colors, self.character_selection,
                                       self.interactive)
        self.eyes_picker = ColorPicker((self.clipboard_padding, 178), Data.eyes_colors, self.character_selection,
                                       self.interactive)
        self.hair_picker = ColorPicker((self.clipboard_padding, 234), Data.hairstyle_colors["normal"],
                                       self.character_selection, self.interactive)
        self.outfit_picker = ColorPicker((self.clipboard_padding, 290), Data.outfit_colors[self.avatar.outfit],
                                         self.character_selection, self.interactive)

        self.left_hair = Image((377, 218), Assets.images_character_creation["left_button_temp"],
                               self.character_selection, self.interactive)
        self.right_hair = Image((513, 218), Assets.images_character_creation["right_button_temp"],
                                self.character_selection, self.interactive)
        self.left_outfit = Image((377, 267), Assets.images_character_creation["left_button_temp"],
                                 self.character_selection, self.interactive)
        self.right_outfit = Image((513, 267), Assets.images_character_creation["right_button_temp"],
                                  self.character_selection, self.interactive)

        # Tabs
        self.selection_tab = Tab((65, 71), "character", self.default_group, self.interactive)
        self.info_tab = Tab((94, 71), "data", self.default_group, self.interactive)
        self.selection_tab.state = "opened"

        self.name_label = NameLabel((self.clipboard_padding, 134.5), self.character_info, self.interactive)

        self.left_pronoun = Image((119 + 3, 244), Assets.images_character_creation["left_button_temp"],
                                  self.character_info, self.interactive)
        self.right_pronoun = Image((232 + 3, 244),
                                   Assets.images_character_creation["right_button_temp"], self.character_info,
                                   self.interactive)
        self.pronoun_index = 0
        self.pronoun_icons = [Assets.images_character_creation["el"], Assets.images_character_creation["ella"],
                              Assets.images_character_creation["elle"]]
        self.pronouns = ["el", "ella", "elle"]
        self.pronoun_icon = Image((self.clipboard_padding, 244),
                                  self.pronoun_icons[self.pronoun_index], self.character_info)

        # GUIImage("name_label", (176, 134.5), assets.images_character_creation["name_label"], self.character_info)
        Text((176, 197), "Mis pronombres son", 32, Colors.SPRITE, self.character_info, shadow=False)
        self.instructions = Text((self.clipboard_padding, 278 + 7.5), "[presiona la tecla F para firmar]", 16,
                                 "#2e2e2e", self.character_info, shadow=False, opacity=63)
        self.character_name = Text((175, 305.5), "", 16, Colors.SPRITE, self.character_info, shadow=False)

        self.active_tab = "selection"
        Window.set_cursor("arrow")

    def draw_signature(self, name: str):
        offset = 0
        width = (21 * len(name)) + (1 * (len(name) - 1))
        surface = pygame.Surface((width, 30), pygame.SRCALPHA)
        joints = []
        for l_index, letter in enumerate(name):
            points = alphabet_dict[letter.lower()]
            lines = []
            for index, point in enumerate(points):
                if index == len(points) - 1:
                    break
                start_x = (point[0] * 3) + offset
                start_y = (point[1] * 3)
                end_x = (points[index + 1][0] * 3) + offset
                end_y = (points[index + 1][1] * 3)
                lines.append(math.dist((start_x, start_y), (end_x, end_y)))
                pygame.draw.line(surface, BLACK_SPRITE, (start_x, start_y), (end_x, end_y), 2)
            if l_index != len(name) - 1:
                final_x = (points[-1][0] * 3) + offset
                final_y = (points[-1][1] * 3)
                next_x = (alphabet_dict[name[l_index + 1].lower()][0][0] * 3) + offset + 20
                next_y = (alphabet_dict[name[l_index + 1].lower()][0][1] * 3)
                joints.append(math.dist((final_x, final_y), (next_x, next_y)))
                pygame.draw.line(surface, BLACK_SPRITE, (final_x, final_y), (next_x, next_y), 2)

            offset += 20
        return surface

    def update(self) -> None:
        self.default_group.update()
        self.avatar.play()
        self.avatar.body = self.skin_picker.selected_color
        self.avatar.eyes = self.eyes_picker.selected_color
        self.avatar.outfit_color = self.outfit_picker.selected_color
        self.avatar.hairstyle_color = self.hair_picker.selected_color

        if any([sprite.hovered for sprite in self.interactive.sprites()]):
            Window.set_cursor("hand")
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
        else:
            Window.set_cursor("arrow")

        if self.selection_tab.clicked and self.active_tab == "info":
            self.active_tab = "selection"
            self.info_tab.state = "hidden"
            self.selection_tab.state = "opened"
        elif self.info_tab.clicked and self.active_tab == "selection":
            self.active_tab = "info"
            self.info_tab.state = "opened"
            self.selection_tab.state = "hidden"

        if self.active_tab == "selection":
            self.character_selection.update()
            # Change Hair
            hair_changed = False
            if self.left_hair.clicked:
                self.avatar.previous_hairstyle()
                hair_changed = True
            elif self.right_hair.clicked:
                self.avatar.next_hairstyle()
                hair_changed = True
            if hair_changed:
                if self.avatar.hairstyle in range(0, 26):
                    self.hair_picker.colors = Data.hairstyle_colors["normal"]
                else:
                    self.hair_picker.colors = Data.hairstyle_colors["dyed"]
            # Change outfit
            if self.left_outfit.clicked:
                self.avatar.previous_outfit()
                self.outfit_picker.colors = Data.outfit_colors[self.avatar.outfit]
            elif self.right_outfit.clicked:
                self.avatar.next_outfit()
                self.outfit_picker.colors = Data.outfit_colors[self.avatar.outfit]

        elif self.active_tab == "info":
            if Input.mouse.buttons["left"] and self.name_label.writing:
                self.name_label.writing = False
            self.character_info.update()

            self.character_name.text = self.name_label.text

            pronoun_changed = False
            if self.left_pronoun.clicked:
                self.pronoun_index -= 1
                pronoun_changed = True
            elif self.right_pronoun.clicked:
                self.pronoun_index += 1
                pronoun_changed = True

            if pronoun_changed:
                if self.pronoun_index >= len(self.pronoun_icons):
                    self.pronoun_index = 0
                elif self.pronoun_index < 0:
                    self.pronoun_index = 2
                self.pronoun_icon.image = self.pronoun_icons[self.pronoun_index]

            self.start_game()

    def start_game(self):
        if self.character_name.text == "":
            return
        if self.name_label.writing:
            return
        if Input.keyboard.key_pressed not in ["F", "f"]:
            return
        from engine.scene.scene_manager import SceneManager
        if SceneManager.transitioning:
            return
        Image((self.clipboard_padding, 283), self.draw_signature(self.character_name.text), self.default_group)
        self.instructions.kill()
        save_manager.active_save.name = self.character_name.text
        save_manager.active_save.pronoun = self.pronouns[self.pronoun_index]
        save_manager.save()

        PlayerData.name = save_manager.active_save.name
        PlayerData.load(save_manager.active_save.money, save_manager.active_save.inventory,
                        save_manager.active_save.tasks)
        PlayerData.pronoun = save_manager.active_save.pronoun
        PlayerData.tutorials = save_manager.active_save.tutorials
        self.avatar.save_character()
        from src.scenes.world.time_manager import TimeManager
        TimeManager.current_day_of_week = save_manager.active_save.week_day
        SceneManager.change_scene(Loading(Data.load_world, World), True, True)
        AudioManager.play_music("exploration")

    @staticmethod
    def get_prevalent_color(surface: pygame.Surface):
        colors = {}
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                color = surface.get_at((x, y))
                color_tuple = tuple(color)

                if color == (58, 58, 80, 255) or color == (58, 58, 80, 0) or color == (0, 0, 0, 0):
                    continue

                if color_tuple not in colors:
                    colors[color_tuple] = 1
                else:
                    colors[color_tuple] += 1
        prevalent_color = max(colors, key=colors.get)
        prevalent_color_rgb = pygame.Color(prevalent_color).rgb
        return prevalent_color_rgb

    def render(self) -> None:
        self.default_group.render(self.display)
        if self.active_tab == "selection":
            self.character_selection.render(self.display)
        elif self.active_tab == "info":
            self.character_info.render(self.display)
            pygame.draw.line(self.display, BLACK_SPRITE, (126, 298), (224, 298))
