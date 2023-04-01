import pygame
import src.engine.assets as assets
from src.game_object.sprite import Sprite, SpriteGroup
from src.constants.colors import *
from src.gui.text import GUIText


class ArrowButton(Sprite):
    def __init__(self, position: tuple, direction: str, *groups: SpriteGroup):
        super().__init__(f"arrowButton_{direction}", position, assets.images_main_menu["arrow_button"], *groups)
        if direction == "right":
            self.flip = True, False
        self.normal_image = self.image.copy()
        mask = pygame.mask.from_surface(self.image)
        self.hover_image = mask.to_surface(setcolor=BLACK_MOTION, unsetcolor=WHITE_MOTION)

    def update(self):
        if self.hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image


class TextButton(Sprite):
    def __init__(self, text: str, position: tuple, *groups: SpriteGroup):
        super().__init__(f"button_{text}", position, pygame.Surface(assets.fonts["monogram"].size(text, 32)), *groups)
        self.image.fill(BLACK_MOTION)
        self.centered = False
        self.text = GUIText(text, self.rect.center, 32, *groups, shadow=False, color=BLUE_MOTION)
        self.updateAll = False

    def update(self):
        if self.hovered:
            self.image.fill(WHITE_MOTION)
            self.text.text_color = BLACK_MOTION
            if not self.updateAll:
                self.updateAll = True
        elif self.updateAll:
            self.image.fill(BLACK_MOTION)
            self.text.text_color = BLUE_MOTION


class ExitButton(Sprite):
    def __init__(self, position: tuple, *groups: SpriteGroup):
        super().__init__("exit_button", position, assets.images_main_menu["close_icon"], *groups)
        self.centered = False
        self.normal_image = self.image.copy()
        mask = pygame.mask.from_surface(self.image)
        self.hover_image = mask.to_surface(setcolor=BLACK_MOTION, unsetcolor=WHITE_MOTION)

    def update(self):
        if self.hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image


class DescriptionTitle(GUIText):
    def __init__(self, position: tuple, text: str, *groups: SpriteGroup):
        super().__init__(text, position, 16, *groups)
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if value != self.text:
            self._text = value
            self.textSurface = assets.fonts["monogram"].render(self._text, 16, WHITE_MOTION)
            self.image = pygame.Surface(
                (self.textSurface.get_width() + 6, self.textSurface.get_height() + 4))
            self.image.fill(BLACK_MOTION)
            x = self.image.get_width() / 2 - self.textSurface.get_width() / 2
            y = self.image.get_height() / 2 - self.textSurface.get_height() / 2
            self.image.blit(self.textSurface, (x, y))

