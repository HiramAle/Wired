import pygame
from engine.time import Time, Timer
from engine.assets import Assets
from src.constants.colors import *
from random import randint, choice
from engine.objects.sprite import Sprite, SpriteGroup, GameObject
from engine.ui.text import Text
from engine.ui.ui_element import UIElement


class RouterLed(Sprite):
    def __init__(self, position: tuple, *groups: SpriteGroup, **kwargs):
        super().__init__(position, pygame.Surface((4, 4)), *groups, **kwargs)
        self.colorOn = "#7eb55d"
        self.colorOff = "#474b75"
        self.image.fill(choice([self.colorOn, self.colorOff]))
        self.timer = Timer(randint(1, 2))
        self.timer.start()
        self.pivot = self.Pivot.TOP_LEFT

    def update(self):
        if self.timer.update():
            self.timer = Timer(randint(1, 2))
            self.timer.start()
            self.image.fill(choice([self.colorOn, self.colorOff]))


class Cloud(Sprite):
    def __init__(self, position: tuple, *groups):
        super().__init__(position, Assets.images_main_menu["cloud"], *groups)
        self.speed = randint(10, 15)
        self.layer = 1

    def update(self):
        self.x += self.speed * Time.dt
        if self.x > 700:
            self.kill()


class CloudGenerator(GameObject):
    def __init__(self, position: tuple, group: SpriteGroup):
        super().__init__(position=position)
        self.group = group
        self.centered = False
        self.timer = Timer(6)
        self.timer.start()
        Cloud((self.x, randint(0, 140)), self.group)

    def update(self):
        if self.timer.update():
            self.timer.start()
            Cloud((self.x, randint(0, 140)), self.group)


class Option(UIElement):
    def __init__(self, option_name: str, position: tuple, *groups: SpriteGroup, **kwargs):
        super().__init__(position, pygame.Surface((310, 30)), *groups, **kwargs)
        self.image.fill(BLACK_MOTION)
        self.pivot = self.Pivot.TOP_LEFT
        self.text = Text(self.rect.center, option_name, 32, BLUE_MOTION, shadow=False, layer=4, parent=self)

    def update(self):
        if self.hovered:
            self.image.fill(WHITE_MOTION)
            self.text.text_color = BLACK_MOTION
        else:
            self.image.fill(BLACK_MOTION)
            self.text.text_color = BLUE_MOTION

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display)
        self.text.render(display)
