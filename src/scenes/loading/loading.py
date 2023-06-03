import pygame
from engine.assets import Assets
from engine.scene.scene import Scene
from threading import Thread, Event
from engine.objects.sprite import Sprite, SpriteGroup
from src.constants.colors import *
from engine.animation.animation import Animation
from engine.ui.text import Text
from engine.ui.image import Image


class Intro(Sprite):
    def __init__(self, position: tuple, animation: Animation, *groups):
        super().__init__(position, animation.current_frame, *groups)
        self.animation = animation

    def update(self):
        self.animation.update()
        self.image = self.animation.current_frame


class Point(Sprite):
    def __init__(self, position: tuple, *groups: SpriteGroup):
        super().__init__(position, pygame.Surface((6, 8)), *groups)
        self.image = pygame.Surface((6, 8))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, DARK_BLACK_MOTION, pygame.Rect(0, 2, 6, 6))
        pygame.draw.rect(self.image, WHITE_MOTION, pygame.Rect(0, 0, 6, 6))


class Loading(Scene):
    def __init__(self, loading_function: callable, scene: type[Scene], thread_args: tuple = None,
                 scene_args: tuple = None):
        super().__init__("loading_scene")
        self.thread_args = thread_args if thread_args is not None else ()
        self.scene_args = scene_args if scene_args is not None else ()
        self.next_scene = scene
        self.loading = Event()
        self.loading.set()
        Thread(name="loading", target=loading_function, args=[self.loading, *self.thread_args]).start()
        self.transitionPosition = 440, 180
        pygame.mouse.set_visible(False)
        self.sprites = SpriteGroup()
        self.veilSurface = self.display.copy()
        self.veilSurface.set_colorkey(GREEN_MOTION)
        Text((200, 180), "CARGANDO", 48, WHITE_MOTION, self.sprites)
        self.crt_effect = Image((0, 0), Assets.images_misc["crt"])
        self.crt_effect.pivot = self.crt_effect.Pivot.TOP_LEFT
        for i in range(3):
            Point((160 + i * 40, 220), self.sprites)
        self.animation = Intro((440, 180), Assets.animations["loading"]["intro"], self.sprites)
        self.swap = False

    def render(self) -> None:
        self.display.fill(DARK_BLACK_MOTION)
        self.sprites.render(self.display)

    def update(self) -> None:
        self.sprites.update()
        if not self.loading.is_set() and not self.swap:
            self.swap = True
            from engine.scene.scene_manager import SceneManager
            SceneManager.change_scene(self.next_scene(*self.scene_args), swap=True, transition=True)
