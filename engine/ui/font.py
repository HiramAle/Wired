import pygame
from typing import Literal
from src.constants.colors import WHITE_MOTION


class Font:
    def __init__(self, name: str, filename: str):
        self.name = name
        self.filename = filename
        self._sizes = (16, 32, 48, 64)
        self.fonts: dict[int, pygame.Font] = {size: pygame.Font(filename, size) for size in self._sizes}

    def size(self, text: str, font_size: Literal[16, 32, 48]) -> tuple[int, int]:
        return self.fonts[font_size].size(text)

    def width(self, text: str, font_size: Literal[16, 32, 48]) -> int:
        return self.fonts[font_size].size(text)[0]

    def height(self, text: str, font_size: Literal[16, 32, 48]) -> int:
        return self.fonts[font_size].size(text)[1]

    def render(self, text: str, size: Literal[16, 32, 48] = 16, color=WHITE_MOTION, wrap_length=0, italic=False):
        try:
            if italic:
                self.fonts[size].italic = True
            return self.fonts[size].render(text, False, color, None, wrap_length)
        finally:
            if italic:
                self.fonts[size].italic = False
