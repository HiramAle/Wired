import pygame
from engine.assets import Assets
from engine.scene.scene import StagedScene, Stage
from engine.objects.sprite import SpriteGroup
from src.constants.colors import *
from src.scenes.main_menu.main_menu_objects import CloudGenerator, RouterLed
from src.scenes.main_menu.main_stage import MainMenuStage
from engine.ui.image import Image


class MainMenu(StagedScene):
    def __init__(self):
        super().__init__("main_menu")
        self._stages: list[Stage] = []
        pygame.mouse.set_visible(True)
        # Groups
        self.visual = SpriteGroup()
        self.foreground = SpriteGroup()
        self.leds = SpriteGroup()
        Image((0, 0), Assets.images_main_menu["sky"], self.visual, centered=False, layer=0)
        self.clouds = CloudGenerator((400, 60), self.visual)
        computer_background = pygame.Surface((310, 240))
        computer_background.fill(BLACK_MOTION)
        Image((96, 52), computer_background, self.visual, centered=False, layer=2)
        # Leds
        for i in range(3):
            RouterLed((494 + i * 6, 272), self.leds)
        # CRT Effect
        crt_image = pygame.Surface((310, 240))
        crt_image.blit(Assets.images_misc["crt"], (0, 0))
        Image((96, 52), crt_image, self.foreground, centered=False, layer=0, flags=pygame.BLEND_RGBA_MULT)
        Image((0, 0), Assets.images_main_menu["pc"], self.foreground, centered=False, layer=1)
        self.set_stage(MainMenuStage(self))

    def update(self) -> None:
        self.current_stage.update()
        self.clouds.update()
        self.visual.update()
        self.leds.update()

    def render(self) -> None:
        self.display.fill(BLACK_MOTION)
        self.visual.render(self.display)
        self.current_stage.render()
        self.foreground.render(self.display)
        self.leds.render(self.display)
