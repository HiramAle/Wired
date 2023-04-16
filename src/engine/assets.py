import pygame
import time
from threading import Thread
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
images_character_creation: dict[str, pygame.Surface] = {}
# Character creation
# skin_tone/action/direction/frames
bodies: dict[int, dict[str, list[pygame.Surface]]] = {}
# eye_color/action/direction/frames
eyes: dict[int, dict[str, list[pygame.Surface]]] = {}
# hairstyle/color/action/direction/frames
hairstyles: dict[int, dict[int, dict[str, list[pygame.Surface]]]] = {}
# outfit/color/action/direction/frames
outfits: dict[int, dict[int, dict[str, list[pygame.Surface]]]] = {}


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
    global images_main_menu, images_selector, images_cables, images_subnetting, images_character_creation
    images_main_menu = load_image_directory(IMAGES_MAIN_MENU)
    images_selector = load_image_directory(IMAGES_SELECTOR)
    images_cables = load_image_directory(IMAGES_CABLES)
    images_subnetting = load_image_directory(IMAGES_SUBNETTING)
    images_character_creation = load_image_directory(IMAGES_CHARACTER_CREATION)
    # load_character_creation_assets()


def load_character_creation_assets():
    def load_bodies():
        global bodies
        bodies = import_category_animations("bodies")

    def load_eyes():
        global eyes
        eyes = import_category_animations("eyes")

    def load_hairstyles():
        global hairstyles
        hairstyles = import_category_animations("hairstyles")

    def load_outfits():
        global outfits
        outfits = import_category_animations("outfits")

    start_time = time.time()
    bodies_thread = Thread(target=load_bodies)
    eyes_thread = Thread(target=load_eyes)
    hairstyles_thread = Thread(target=load_hairstyles)
    outfits_thread = Thread(target=load_outfits)

    bodies_thread.start()
    eyes_thread.start()
    hairstyles_thread.start()
    outfits_thread.start()

    bodies_thread.join()
    eyes_thread.join()
    hairstyles_thread.join()
    outfits_thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time} segundos")

    # for body, directions in bodies.items():
    #     print(body, end=": ")
    #     for direction in directions:
    #         print(direction, ":", bodies[body][direction])

    # start_time = time.time()
    # all_animations = import_character_generator()
    # bodies = all_animations["bodies"]
    # eyes = all_animations["eyes"]
    # hairstyles = all_animations["hairstyles"]
    # outfits = all_animations["outfits"]
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Tiempo de ejecución: {elapsed_time} segundos")
