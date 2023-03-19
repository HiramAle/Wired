import pygame
from src.utils.load import load_cursor
from src.constants.paths import *

# ---------- Assets ----------
cursors: dict[str, pygame.cursors.Cursor] = {}


def prepare() -> None:
    """
    Preloads light resources before the heavy load, in order to improve performance.
    :return: None
    """
    global cursors
    cursors = load_cursor(CURSORS)
