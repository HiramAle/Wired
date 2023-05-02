import math
import random

import pygame
import src.engine.assets as assets
import src.engine.input as input
from src.game_object.sprite import Sprite, SpriteGroup
from src.constants.colors import *


class Color(Sprite):
    def __init__(self, position: tuple, index: int, color: tuple | str, *groups, **kwargs):
        image = pygame.Surface((22, 22), pygame.SRCALPHA)
        image.fill(color)
        image.blit(assets.images_character_creation["color_selection"], (0, 0))
        super().__init__("color", position, image, *groups, **kwargs)
        self.index = index
        self.color = color

    def render(self, display: pygame.Surface, offset=(0, 0)):
        if self.hovered:
            mask = pygame.mask.from_surface(self.image)
            mask_surface = mask.to_surface(setcolor=WHITE_MOTION, unsetcolor=(0, 0, 0))
            mask_surface.set_colorkey((0, 0, 0))
            display.blit(mask_surface, (self.rect.x - 2, self.rect.y))
            display.blit(mask_surface, (self.rect.x + 2, self.rect.y))
            display.blit(mask_surface, (self.rect.x, self.rect.y - 2))
            display.blit(mask_surface, (self.rect.x, self.rect.y + 2))
        super().render(display)


class ColorPicker(Sprite):
    def __init__(self, position: tuple, colors: dict[int, tuple], *groups, **kwargs):
        image = pygame.Surface((274, 30), pygame.SRCALPHA)
        super().__init__("color_picker", position, image, *groups, **kwargs)
        self._colors: dict[int, tuple] = {}
        self.color_group = SpriteGroup()
        self.color_spacing = 5
        self.total_width = 0
        self.remaining_space = 0
        self.starting_position = 0
        # self._image.fill((255, 0, 0, 30))
        self.selected_color = 0
        self.interactive_group: SpriteGroup = groups[1]
        self.remove(self.interactive_group)
        self.colors = colors

    def randomize(self):
        self.selected_color = random.choice(list(self._colors.keys()))

    @property
    def colors(self) -> dict:
        return self._colors

    @colors.setter
    def colors(self, value: dict):
        self.color_group = SpriteGroup()
        self.selected_color = 0
        self.total_width = len(value) * 22 + (len(value) - 1) * self.color_spacing
        self.remaining_space = self.width - self.total_width
        self.starting_position = self.remaining_space / 2 + 11
        for index, color in enumerate(value.values()):
            x = self.rect.left + self.starting_position + (index * (22 + self.color_spacing))
            y = self.rect.top + self.height / 2
            Color((x, y), index, color, self.color_group, self.interactive_group)
        self._colors = value

    def update(self, *args, **kwargs):
        for color in self.color_group.sprites():
            color: Color
            if color.clicked:
                self.selected_color = color.index

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display, offset)
        self.color_group.render(display)
