import pygame
import src.engine.time as time
import src.engine.assets as assets
import src.engine.window as window
from src.constants.colors import *
from random import randint, choice
from src.game_object.sprite import Sprite, SpriteGroup, GameObject
from src.gui.text import GUIText


class RouterLed(Sprite):
    def __init__(self, position: tuple, *groups: SpriteGroup, **kwargs):
        super().__init__("routerLed", position, pygame.Surface((4, 4)), *groups, **kwargs)
        self.colorOn = "#7eb55d"
        self.colorOff = "#474b75"
        self.image.fill(choice([self.colorOn, self.colorOff]))
        self.timer = time.Timer(randint(1, 2))
        self.timer.start()
        self.centered = False

    def update(self):
        if self.timer.update():
            self.timer = time.Timer(randint(1, 2))
            self.timer.start()
            self.image.fill(choice([self.colorOn, self.colorOff]))


class Cloud(Sprite):
    def __init__(self, position: tuple, *groups):
        super().__init__("cloud", position, assets.images_main_menu["cloud"], *groups)
        self.speed = randint(10, 15)
        self.layer = 1

    def update(self):
        self.x += self.speed * time.dt
        if self.x > 700:
            self.kill()


class CloudGenerator(GameObject):
    def __init__(self, position: tuple, group: SpriteGroup):
        super().__init__("cloud_generator", position, (10, 140))
        self.group = group
        self.centered = False
        self.timer = time.Timer(6)
        self.timer.start()

    def update(self):
        if self.timer.update():
            self.timer.start()
            Cloud((self.x, randint(0, 140)), self.group)


class Option(Sprite):
    def __init__(self, option_name: str, position: tuple, *groups: SpriteGroup, **kwargs):
        super().__init__(option_name, position, pygame.Surface((310, 30)), *groups, **kwargs)
        self.image.fill(BLACK_MOTION)
        self.centered = False
        self.interactive = True
        self.text = GUIText(option_name, self.rect.center, 32, *groups, shadow=False, color=BLUE_MOTION, layer=4)

    def update(self):
        if self.hovered:
            self.image.fill(WHITE_MOTION)
            self.text.text_color = BLACK_MOTION
        else:
            self.image.fill(BLACK_MOTION)
            self.text.text_color = BLUE_MOTION


