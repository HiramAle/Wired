import pygame
from src.test.singleton.preferences import instance as preferences


class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface((0, 0))

    def init(self):
        self.screen = pygame.display.set_mode((preferences.window_width, preferences.window_height))
        pygame.display.set_caption("Window")


instance = Window()
