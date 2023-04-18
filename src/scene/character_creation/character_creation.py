import json
import math

import pygame
import src.engine.assets as assets
import src.engine.input as game_input
import src.engine.data as data
from src.scene.core.scene import Scene
from src.game_object.sprite import SpriteGroup
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.scene.character_creation.avatar import Avatar
from src.scene.character_creation.colors import ColorPicker
from src.constants.colors import *
from src.scene.character_creation.character_objects import Tab, NameLabel
import random

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
        GUIImage("background", (0, 0), assets.images_character_creation["players_house_background"], self.default_group,
                 centered=False)
        self.clipboard = GUIImage("clipboard", (21, 31), assets.images_character_creation["clip_board"],
                                  self.default_group, centered=False)
        self.avatar = Avatar(self.default_group)
        table_image = pygame.Surface((274, 309), pygame.SRCALPHA)
        table_image.fill((122, 73, 76, 48))
        self.clipboard_padding = self.clipboard.rect.centerx + 3
        GUIText("Piel", (self.clipboard_padding, 94), 32, self.character_selection, color=BLACK_SPRITE, shadow=False)
        GUIText("Ojos", (self.clipboard_padding, 150), 32, self.character_selection, color=BLACK_SPRITE, shadow=False)
        GUIText("Color de cabello", (self.clipboard_padding, 206), 32, self.character_selection, color=BLACK_SPRITE,
                shadow=False)
        GUIText("Color de ropa", (self.clipboard_padding, 262), 32, self.character_selection, color=BLACK_SPRITE,
                shadow=False)

        self.skin_picker = ColorPicker((self.clipboard_padding, 122), data.body_colors, self.character_selection)
        self.eyes_picker = ColorPicker((self.clipboard_padding, 178), data.eyes_colors, self.character_selection)
        self.hair_picker = ColorPicker((self.clipboard_padding, 234), data.hairstyle_colors["normal"],
                                       self.character_selection)
        self.outfit_picker = ColorPicker((self.clipboard_padding, 290), data.outfit_colors[self.avatar.outfit],
                                         self.character_selection)

        self.left_hair = GUIImage("left_hair", (377, 218), assets.images_character_creation["left_button_temp"],
                                  self.character_selection)
        self.right_hair = GUIImage("left_hair", (513, 218), assets.images_character_creation["right_button_temp"],
                                   self.character_selection)
        self.left_outfit = GUIImage("left_outfit", (377, 267), assets.images_character_creation["left_button_temp"],
                                    self.character_selection)
        self.right_outfit = GUIImage("right_outfit", (513, 267), assets.images_character_creation["right_button_temp"],
                                     self.character_selection)

        # Tabs
        self.selection_tab = Tab((65, 71), "character", self.default_group)
        self.info_tab = Tab((94, 71), "data", self.default_group)
        self.selection_tab.state = "opened"

        self.name_label = NameLabel((self.clipboard_padding, 134.5), self.character_info)

        self.left_pronoun = GUIImage("left_pronoun", (119 + 3, 244),
                                     assets.images_character_creation["left_button_temp"],
                                     self.character_info)
        self.right_pronoun = GUIImage("right_pronoun", (232 + 3, 244),
                                      assets.images_character_creation["right_button_temp"], self.character_info)
        self.pronoun_index = 0
        self.pronoun_icons = [assets.images_character_creation["el"], assets.images_character_creation["ella"],
                              assets.images_character_creation["elle"]]
        self.pronoun_icon = GUIImage("pronoun_icon", (self.clipboard_padding, 244),
                                     self.pronoun_icons[self.pronoun_index], self.character_info)

        # GUIImage("name_label", (176, 134.5), assets.images_character_creation["name_label"], self.character_info)
        GUIText("Mis pronombres son", (176, 197), 32, self.character_info, color=BLACK_SPRITE, shadow=False)
        self.instructions = GUIText("[presiona la tecla F para firmar]", (self.clipboard_padding, 278 + 7.5), 16,
                                    self.character_info,
                                    color="#2e2e2e", shadow=False, opacity=63)
        self.name = GUIText("", (175, 305.5), 16, self.character_info, shadow=False, color=BLACK_SPRITE)

        self.active_tab = "selection"

    def draw_signature(self, name: str):
        offset = 0
        width = (21 * len(name)) + (1 * (len(name) - 1))
        print("width", width)
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
            else:
                print("max", letter, max(lines) + offset)
            if joints:
                print("max_joint", letter, max(joints) + offset)
            offset += 20
        return surface

    def update(self) -> None:
        self.default_group.update()

        self.avatar.play()
        self.avatar.body = self.skin_picker.selected_color
        self.avatar.eyes = self.eyes_picker.selected_color
        self.avatar.outfit_color = self.outfit_picker.selected_color
        self.avatar.hairstyle_color = self.hair_picker.selected_color

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
                    self.hair_picker.colors = data.hairstyle_colors["normal"]
                else:
                    self.hair_picker.colors = data.hairstyle_colors["dyed"]
            # Change outfit
            if self.left_outfit.clicked:
                self.avatar.previous_outfit()
                self.outfit_picker.colors = data.outfit_colors[self.avatar.outfit]
            elif self.right_outfit.clicked:
                self.avatar.next_outfit()
                self.outfit_picker.colors = data.outfit_colors[self.avatar.outfit]

            # if game_input.keyboard.keys["space"]:
            #     self.avatar.randomize()
            #     self.outfit_picker.colors = data.outfit_colors[self.avatar.outfit]
            #     if self.avatar.hairstyle in range(0, 26):
            #         self.hair_picker.colors = data.hairstyle_colors["normal"]
            #     else:
            #         self.hair_picker.colors = data.hairstyle_colors["dyed"]
            #     self.skin_picker.randomize()
            #     self.eyes_picker.randomize()
            #     self.outfit_picker.randomize()
            #     self.hair_picker.randomize()

        elif self.active_tab == "info":
            if game_input.mouse.buttons["left"] and self.name_label.writing:
                self.name_label.writing = False
            self.character_info.update()

            self.name.text = self.name_label.text

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

            # self.name_label.text = "1"
            # print(self.name_label.text)

            # elif input.keyboard.keys["space"]:
            #     self.avatar.save_character()

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
            if self.name.text != "" and game_input.keyboard.key_pressed in ["F", "f"]:
                GUIImage("test", (self.clipboard_padding, 283), self.draw_signature(self.name.text), self.default_group)
                self.instructions.kill()
