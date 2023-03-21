import pygame
from src.utils.load import *
from src.gui.font import Font
from src.game_object.components import Animation
from src.constants.paths import *

# ---------- Assets ----------
cursors: dict[str, pygame.cursors.Cursor] = {}
fonts: dict[str, Font] = {}
images_misc: dict[str, pygame.Surface] = {}
animations: dict[str, dict[str, list]] = {}


def prepare() -> None:
    """
    Preloads light resources before the heavy load, in order to improve performance.
    :return: None
    """
    global cursors, fonts, images_misc, animations
    cursors = load_cursors(CURSORS)
    fonts = load_fonts(FONTS)
    images_misc = load_image_directory(IMAGES_MISC)
    animations = load_animations(ANIMATIONS)


def load() -> None:
    ...
