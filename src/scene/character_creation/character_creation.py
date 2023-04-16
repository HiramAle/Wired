import json
import pygame
import src.engine.assets as assets
import src.engine.input as input
import src.engine.data as data
from src.scene.core.scene import Scene
from src.game_object.sprite import SpriteGroup
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.scene.character_creation.avatar import Avatar
from src.scene.character_creation.colors import ColorPicker


class CharacterCreation(Scene):
    def __init__(self):
        super().__init__("character_creation")
        pygame.mouse.set_visible(True)
        self.group = SpriteGroup()
        GUIImage("background", (-581, -893), assets.images_character_creation["players_house"], self.group, scale=2,
                 centered=False, layer=0)
        self.avatar = Avatar(self.group)
        table_image = pygame.Surface((274, 309), pygame.SRCALPHA)
        table_image.fill((122, 73, 76, 48))
        self.table = GUIImage("table", (39, 32), table_image, self.group, centered=False)
        GUIText("Skin tone", (self.table.rect.centerx, 132), 32, self.group)
        GUIText("Hair color", (self.table.rect.centerx, 194), 32, self.group)
        GUIText("Outfit color", (self.table.rect.centerx, 256), 32, self.group)
        self.skin_picker = ColorPicker((self.table.rect.centerx, 163), data.body_colors, self.group)
        self.eyes_picker = ColorPicker((self.table.rect.centerx, 194), data.eyes_colors, self.group)
        self.outfit_picker = ColorPicker((self.table.rect.centerx, 256), data.outfit_colors[self.avatar.outfit],
                                         self.group)
        self.hair_picker = ColorPicker((self.table.rect.centerx, 286), data.hairstyle_colors["normal"], self.group)

    def update(self) -> None:
        self.group.update()
        self.avatar.play()

        self.avatar.body = self.skin_picker.selected_color
        self.avatar.eyes = self.eyes_picker.selected_color
        self.avatar.outfit_color = self.outfit_picker.selected_color
        self.avatar.hairstyle_color = self.hair_picker.selected_color

        if input.keyboard.keys["interact"]:
            self.avatar.next_hairstyle()

            if self.avatar.hairstyle in range(0, 26):
                self.hair_picker.colors = data.hairstyle_colors["normal"]
            else:
                self.hair_picker.colors = data.hairstyle_colors["dyed"]

        elif input.keyboard.keys["esc"]:
            self.avatar.next_outfit()
            self.outfit_picker.colors = data.outfit_colors[self.avatar.outfit]
            print(self.outfit_picker.selected_color)

        elif input.keyboard.keys["space"]:
            self.avatar.save_character()

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
        self.group.render(self.display)
        self.skin_picker.render(self.display)
