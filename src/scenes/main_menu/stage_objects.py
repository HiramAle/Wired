import pygame
from engine.assets import Assets
from engine.objects.sprite import Sprite, SpriteGroup
from src.constants.colors import *
from engine.ui.text import Text


class ArrowButton(Sprite):
    def __init__(self, position: tuple, direction: str, *groups: SpriteGroup):
        super().__init__(position, Assets.images_main_menu["arrow_button"], *groups)
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
        super().__init__(position, pygame.Surface(Assets.fonts["monogram"].size(text, 32)), *groups)
        self.image.fill(BLACK_MOTION)
        self.centered = False
        self.text = Text(self.rect.center, text, 32, BLUE_MOTION, *groups, shadow=False)
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
        super().__init__(position, Assets.images_main_menu["close_icon"], *groups)
        self.centered = False
        self.normal_image = self.image.copy()
        mask = pygame.mask.from_surface(self.image)
        self.hover_image = mask.to_surface(setcolor=BLACK_MOTION, unsetcolor=WHITE_MOTION)

    def update(self):
        if self.hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image


class DescriptionTitle(Text):
    def __init__(self, position: tuple, text: str, *groups: SpriteGroup):
        super().__init__(position, text, 16, WHITE_MOTION, *groups)
        self.text = text
        self.shadow = False

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if value != self.text:
            self._text = value
            self.textSurface = Assets.fonts["monogram"].render(self._text, 16, WHITE_MOTION)
            self.image = pygame.Surface(
                (self.textSurface.get_width() + 6, self.textSurface.get_height() + 4))
            self.image.fill(BLACK_MOTION)
            x = self.image.get_width() / 2 - self.textSurface.get_width() / 2
            y = self.image.get_height() / 2 - self.textSurface.get_height() / 2
            self.image.blit(self.textSurface, (x, y))
