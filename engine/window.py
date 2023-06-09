import pygame
from ctypes import windll
from os import environ

from engine.preferences import Preferences
from engine.assets import Assets
from engine.constants import Locals
from engine.loader import Loader


class Window:
    width: int
    height: int
    size: tuple
    screen: pygame.Surface

    @classmethod
    def init(cls):
        """
        Initialization method for window handler
        """
        # Deactivate Windows DPI escalation
        windll.user32.SetProcessDPIAware()
        # Set the window centered on screen
        environ['SDL_VIDEO_CENTERED'] = "1"
        cls.width = Preferences.window_width
        cls.height = Preferences.window_height
        cls.size = cls.width, cls.height
        cls.screen = pygame.display.set_mode(cls.size, vsync=1)
        pygame.display.set_caption(Locals.GAME_NAME)
        pygame.display.set_icon(Loader.load_image("assets/images/misc/icon.png"))

    @staticmethod
    def set_cursor(cursor: str):
        if Assets.cursors[cursor] == pygame.mouse.get_cursor():
            return
        pygame.mouse.set_cursor(Assets.cursors[cursor])

    @classmethod
    def set_window_size(cls, size: tuple):
        cls.width, cls.height = size
        cls.size = size
        Preferences.window_width, Preferences.window_height = size
        # Preferences.save()
        cls.screen = pygame.display.set_mode(cls.size)

    @staticmethod
    def update():
        """
        Updates the Pygame display.
        """
        pygame.display.update()
