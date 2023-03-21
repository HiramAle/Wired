import pygame

from src.scene.scene import Scene
import src.engine.input as input
import src.engine.window as window


class MainMenu(Scene):
    def __init__(self):
        super().__init__("main_menu")
        pygame.mouse.set_visible(True)

    def render(self) -> None:
        self.display.fill("red")
