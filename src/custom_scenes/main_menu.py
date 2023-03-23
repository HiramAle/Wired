import pygame
from random import choice, randint
from src.scene.scene import Scene, StagedScene, Stage
from src.game_object.sprite import Sprite, SpriteGroup
from src.game_object.game_object import GameObject
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.constants.colors import *
from src.utils.maths import sin_wave
import src.engine.input as input
import src.engine.window as window
import src.engine.assets as assets
import src.engine.time as time


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

    def on_mouse_enter(self):
        print("enter")
        window.set_cursor("hand")

    def on_mouse_exit(self):
        print("exit")
        window.set_cursor("arrow")


class MainMenuStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("main_menu_stage", scene)
        self.logo = GUIImage("logo", (251, 130), assets.images_misc["logo"], self.group)
        self.newGame = Option("- NEW GAME -", (96, 167), self.group)
        self.continueGame = Option("- CONTINUE -", (96, 197), self.group)
        self.options = Option("- OPTIONS -", (96, 227), self.group)
        self.exit = Option("- EXIT -", (96, 257), self.group)

    def update(self):
        super().update()
        self.logo.y = sin_wave(115, 5, 200)
        if self.options.clicked:
            self.scene.set_stage(OptionsStage(self.scene))


class OptionsStage(Stage):
    def __init__(self, scene: StagedScene):
        super().__init__("options_stage", scene)
        self.group = SpriteGroup()
        GUIText("OPTIONS", (209, 61), 32, self.group, color=WHITE_MOTION, centered=False)
        GUIImage("top_line", (51, 54), assets.images_main_menu["doted_line"], self.group, centered=False)
        GUIImage("bottom_line", (51, 99), assets.images_main_menu["doted_line"], self.group, centered=False)


class MainMenu(StagedScene):
    def __init__(self):
        super().__init__("main_menu")
        self._stages: list[Stage] = []
        pygame.mouse.set_visible(True)
        # Groups
        self.visual = SpriteGroup()
        self.foreground = SpriteGroup()
        GUIImage("sky", (0, 0), assets.images_main_menu["sky"], self.visual, centered=False, layer=0)
        self.add(CloudGenerator((400, 60), self.visual))  # 1
        computer_background = pygame.Surface((310, 240))
        computer_background.fill(BLACK_MOTION)
        GUIImage("pc_bg", (96, 52), computer_background, self.visual, centered=False, layer=2)
        # Leds
        for i in range(3):
            RouterLed((494 + i * 6, 272), self.visual, layer=3)
        # CRT Effect
        crt_image = pygame.Surface((310, 240))
        crt_image.blit(assets.images_misc["crt"], (0, 0))
        GUIImage("crt", (96, 52), crt_image, self.foreground, centered=False, layer=0, flags=pygame.BLEND_RGBA_MULT)
        GUIImage("pc", (0, 0), assets.images_main_menu["pc"], self.foreground, centered=False, layer=1)
        self.set_stage(MainMenuStage(self))

    def update(self) -> None:
        self.update_objects()
        self.visual.update()
        self.current_stage.update()

    def render(self) -> None:
        self.display.fill(BLACK_MOTION)
        self.visual.render(self.display)
        self.current_stage.render()
        self.foreground.render(self.display)
