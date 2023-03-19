import pygame
from ctypes import windll
from os import environ
from src.constants.locals import GAME_NAME
import src.user.preferences as preferences
import src.engine.assets as assets

# Deactivate Windows DPI escalation
windll.user32.SetProcessDPIAware()
# Set the window centered on screen
environ['SDL_VIDEO_CENTERED'] = "1"

# ---------- Window ----------
width = 0
height = 0
screen = pygame.display.set_mode((1, 1))


def init():
    """
    Initialization method for window handler
    """
    global screen, width, height
    width = preferences.window_width
    height = preferences.window_height
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(GAME_NAME)
    pygame.mouse.set_cursor(assets.cursors["arrow"])


def update():
    """
    Updates the Pygame display.
    """
    pygame.display.update()
