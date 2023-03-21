import pygame

from src.scene.scene import Scene
from threading import Thread, Event
from time import sleep
from src.custom_scenes.main_menu import MainMenu
import src.scene.scene_manager as scene_manager


class Loading(Scene):
    def __init__(self):
        super().__init__("loading_scene")
        self.loading = Event()
        Thread(name="loading_assets", target=self.load).start()
        self.transitionPosition = 640, 360
        pygame.mouse.set_visible(False)

    def load(self):
        self.loading.set()
        sleep(2)
        self.loading.clear()

    def render(self) -> None:
        self.display.fill("blue")

    def update(self) -> None:
        if not self.loading.is_set():
            scene_manager.change_scene(self, MainMenu(), swap=True)
