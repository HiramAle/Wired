import pygame
import src.scene.core.scene_manager as scene_manager
import src.engine.assets as assets
from src.scene.core.scene import Scene
from threading import Thread, Event
from time import sleep
from src.scene.main_menu.main_menu import MainMenu
from src.game_object.sprite import Sprite, SpriteGroup
from src.constants.colors import *
from src.gui.text import GUIText
from src.gui.image import GUIImage
from src.components.animation import Animation
from src.scene.cables.order import OrderCable
from src.scene.subnetting.subnetting import Subnetting
from src.scene.map.test_map import TestMap
from src.scene.character_creation.character_creation import CharacterCreation
from src.scene.core.transition import FadeTransition


class Intro(Sprite, Animation):
    def __init__(self, position: tuple, data: list, *groups):
        Animation.__init__(self, data)
        Sprite.__init__(self, "intro", position, self.frame, *groups)

    def update(self):
        self.play()
        self.image = self.frame


class Point(Sprite):
    def __init__(self, position: tuple, *groups: SpriteGroup):
        super().__init__("point", position, pygame.Surface((6, 8)), *groups)
        self.image = pygame.Surface((6, 8))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, DARK_BLACK_MOTION, pygame.Rect(0, 2, 6, 6))
        pygame.draw.rect(self.image, WHITE_MOTION, pygame.Rect(0, 0, 6, 6))


class Loading(Scene):
    def __init__(self, loading_function: callable, scene: type[Scene], thread_args: tuple = None,
                 scene_args: tuple = None):
        super().__init__("loading_scene")
        print(f"transitioning to {scene.__class__.__name__} loading {loading_function}")
        self.thread_args = thread_args if thread_args is not None else ()
        self.scene_args = scene_args if scene_args is not None else ()
        self.next_scene = scene
        self.loading = Event()
        self.loading.set()
        Thread(name="loading_assets", target=loading_function, args=[self.loading, *self.thread_args]).start()
        self.transitionPosition = 440, 180
        pygame.mouse.set_visible(False)
        self.sprites = SpriteGroup()
        self.veilSurface = self.display.copy()
        self.veilSurface.set_colorkey(GREEN_MOTION)
        GUIText("CARGANDO", (200, 180), 48, self.sprites)
        self.crt_effect = GUIImage("crt", (0, 0), assets.images_misc["crt"], centered=False)
        for i in range(3):
            Point((160 + i * 40, 220), self.sprites)
        self.animation = Intro((440, 180), assets.animations["loading"]["intro"], self.sprites)
        self.swap = False

    def render(self) -> None:
        self.display.fill(DARK_BLACK_MOTION)
        self.sprites.render(self.display)

    def update(self) -> None:
        self.sprites.update()
        if not self.loading.is_set() and not self.swap:
            self.swap = True
            scene_manager.change_scene(self, self.next_scene(*self.scene_args), swap=True, transition=True)
