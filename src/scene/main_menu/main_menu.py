import pygame
import src.engine.assets as assets
from src.scene.core.scene import StagedScene, Stage
from src.game_object.sprite import SpriteGroup
from src.gui.image import GUIImage
from src.constants.colors import *
from src.scene.main_menu.main_menu_objects import CloudGenerator, RouterLed
from src.scene.main_menu.main_menu_stages import MainMenuStage


class MainMenu(StagedScene):
    def __init__(self):
        super().__init__("main_menu")
        self._stages: list[Stage] = []
        pygame.mouse.set_visible(True)
        # Groups
        self.visual = SpriteGroup()
        self.foreground = SpriteGroup()
        GUIImage("sky", (0, 0), assets.images_main_menu["sky"], self.visual, centered=False, layer=0)
        self.clouds = CloudGenerator((400, 60), self.visual)  # 1
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
        self.clouds.update()
        self.visual.update()
        self.current_stage.update()

    def render(self) -> None:
        self.display.fill(BLACK_MOTION)
        self.visual.render(self.display)
        self.current_stage.render()
        self.foreground.render(self.display)
