import pygame
from src.utils.load import *
from src.gui.font import Font
from src.components.animation import Animation
from src.constants.paths import *

# ---------- Assets ----------
cursors: dict[str, pygame.cursors.Cursor] = {}
fonts: dict[str, Font] = {}
images_misc: dict[str, pygame.Surface] = {}
animations: dict[str, dict[str, list]] = {}
images_main_menu: dict[str, pygame.Surface] = {}
images_selector: dict[str, pygame.Surface] = {}
images_cables: dict[str, pygame.Surface] = {}
images_subnetting: dict[str, pygame.Surface] = {}


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
    global images_main_menu, images_selector, images_cables, images_subnetting
    images_main_menu = load_image_directory(IMAGES_MAIN_MENU)
    images_selector = load_image_directory(IMAGES_SELECTOR)
    images_cables = load_image_directory(IMAGES_CABLES)
    images_subnetting = load_image_directory(IMAGES_SUBNETTING)
