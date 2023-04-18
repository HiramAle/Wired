import pygame
import src.engine.assets as assets
from src.constants.colors import WHITE_MOTION, DARK_BLACK_MOTION
from src.game_object.sprite import Sprite
from typing import Literal


class GUIText(Sprite):
    def __init__(self, text: str, position: tuple, size: Literal[16, 32, 48, 64], *groups, **kwargs):
        text_surface = assets.fonts["monogram"].render(text, size)
        super().__init__(f"text_{text}", position, text_surface, *groups, **kwargs)
        self._text = text
        self._size = size
        self._color = WHITE_MOTION
        self._shadow_color = DARK_BLACK_MOTION
        self.shadow = True
        self.font = "monogram"
        for name, value in kwargs.items():
            match name:
                case "color":
                    self._color = value
                case "shadow_color":
                    self._shadow_color = value
                case "shadow":
                    self.shadow = value
                case "font":
                    self.font = value
        self._shadow_padding = (size // 16) * 0.75 if self.shadow else 0
        print(self._shadow_padding)
        self.text = text

    def _update_text(self):
        text_surface = assets.fonts[self.font].render(self._text, self._size, self._color)
        self.image = pygame.Surface(
            (text_surface.get_width(), text_surface.get_height() + self._shadow_padding)).convert_alpha()
        self.image.set_alpha(self.opacity)

        if self.shadow:
            shadow_surface = assets.fonts[self.font].render(self._text, self._size, self._shadow_color)
            self.image.blit(shadow_surface, (0, self._shadow_padding))
            # self.image.blit(text_surface, (0, 0))

        self.image.blit(text_surface, (0, -self._shadow_padding))
        self.image.set_colorkey((0, 0, 0))

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self._update_text()

    @property
    def text_color(self) -> tuple | str:
        return self._color

    @text_color.setter
    def text_color(self, value: tuple | str):
        self._color = value
        self._update_text()
