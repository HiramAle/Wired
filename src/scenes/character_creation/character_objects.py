import pygame
from engine.assets import Assets
from engine.input import Input
from engine.objects.sprite import Sprite
from engine.ui.text import Text
from engine.constants import Colors

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U",
           "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p",
           "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


class Tab(Sprite):
    def __init__(self, position: tuple, icon: str, *groups, **kwargs):
        super().__init__(position, Assets.images_character_creation[f"tab_{icon}_hidden"], *groups, **kwargs)
        self._state = "hidden"
        self.icon = icon
        new_rect = self.rect.copy()
        new_rect.bottom = 71
        self.y = new_rect.centery

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: str):
        if self._state == value:
            return
        self._state = value
        self.image = Assets.images_character_creation[f"tab_{self.icon}_{value}"]
        new_rect = self.rect.copy()
        new_rect.bottom = 71
        self.y = new_rect.centery


class NameLabel(Sprite):
    def __init__(self, position: tuple, *groups, **kwargs):
        super().__init__(position, Assets.images_character_creation["name_label"], *groups, **kwargs)
        self._text = Text((self.rect.centerx, self.rect.centery + 10), "", 32, Colors.SPRITE, shadow=False,
                          font="fool")
        self.writing = False

    def update(self, *args, **kwargs):
        if self.clicked and not self.writing:
            self.writing = True

        if self.writing and len(self.text) <= 6:
            if Input.keyboard.key_pressed in letters:
                self.text += Input.keyboard.key_pressed

        if Input.keyboard.keys["backspace"]:
            self.text = self.text[:-1]
        elif Input.keyboard.keys["enter"] or Input.keyboard.keys["esc"]:
            self.writing = False

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=Colors.WHITE, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        if self.centered:
            rect = surface.get_rect(center=self.position)
        else:
            rect = surface.get_rect(topleft=self.position)
        display.blit(surface, (rect.left + 3, rect.top))
        display.blit(surface, (rect.left - 3, rect.top))
        display.blit(surface, (rect.left, rect.top + 3))
        display.blit(surface, (rect.left, rect.top - 3))

    def render(self, display: pygame.Surface, offset=(0, 0)):
        if self.writing:
            self.draw_outline(display)
        super().render(display)
        self._text.render(display)

    @property
    def text(self):
        return self._text.text

    @text.setter
    def text(self, value):
        self._text.text = value
