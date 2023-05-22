import pygame

from engine.ui.ui_element import UIElement
from engine.assets import Assets
from engine.constants import Colors
from typing import Literal


class Text(UIElement):
    def __init__(self, position: tuple, text: str, size: Literal[16, 32, 48, 64],
                 color: str | tuple | pygame.Color = Colors.WHITE, *groups, **kwargs):
        text_surface = Assets.fonts["monogram"].render(text, size, color, kwargs.get("max_width", 0),
                                                       kwargs.get("italic", False))
        super().__init__(position, text_surface, *groups, **kwargs)
        self.__size = size
        self.__text = text
        self.color = color
        self.shadow_color = Colors.DARK
        self.shadow_opacity = kwargs.get("shadow_opacity", 255)
        self.max_width = kwargs.get("max_width", 0)
        self.shadow = False
        self._shadow_padding = (size // 16) * 1.25
        self.font = "monogram"
        self.italic = kwargs.get("italic", False)
        self.shadow_image = Assets.fonts["monogram"].render(text, size, self.shadow_color, self.max_width)
        self.shadow_image.set_alpha(self.shadow_opacity)
        for key, val in kwargs.items():
            if key in ["shadow", "shadow_color", "font"] and hasattr(self, key):
                setattr(self, key, val)

    def __render_text(self):
        self.image = Assets.fonts[self.font].render(self.__text, self.__size, self.color, self.max_width, self.italic)
        self.image.set_alpha(self.opacity)
        if self.shadow:
            self.shadow_image = Assets.fonts["monogram"].render(self.__text, self.__size, self.shadow_color,
                                                                self.max_width, self.italic)
            self.shadow_image.set_alpha(self.shadow_opacity)

    def __copy__(self):
        copy = Text(self.position, self.text, self.__size, self.color)
        copy.image = self.image
        copy.max_width = self.max_width
        copy.shadow = self.shadow
        copy.font = self.font
        copy.shadow_image = self.shadow_image
        copy.pivot = self.pivot
        return copy

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.shadow:
            shadow_rect = self.rect
            shadow_rect.y += self._shadow_padding
            shadow_rect.x += self._shadow_padding
            display.blit(self.shadow_image, shadow_rect)
        super().render(display)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str):
        self.__text = value
        self.__render_text()

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, value: int):
        self.__size = value
        self.__render_text()

    @property
    def text_color(self) -> tuple | pygame.Color | str:
        return self.color

    @text_color.setter
    def text_color(self, value: tuple | pygame.Color | str):
        self.color = value
        self.__render_text()
