import threading
import pygame
from threading import Thread
from src.utils.load import *
from engine.ui.font import Font
from src.constants.paths import *
from engine.animation.animation import Animation
from engine.loader import Loader
from engine.constants import Paths


class Assets:
    cursors: dict[str, pygame.cursors.Cursor] = {}
    music: dict[str, str] = {}
    sounds: dict[str, list[pygame.mixer.Sound]] = {}
    fonts: dict[str, Font] = {}
    images_misc: dict[str, pygame.Surface] = {}
    animations: dict[str, dict[str, Animation]] = {}
    images_main_menu: dict[str, pygame.Surface] = {}
    images_selector: dict[str, pygame.Surface] = {}
    images_cables: dict[str, pygame.Surface] = {}
    images_subnetting: dict[str, pygame.Surface] = {}
    images_character_creation: dict[str, pygame.Surface] = {}
    images_actors: dict[str, pygame.Surface] = {}
    images_world: dict[str, pygame.Surface] = {}
    images_book: dict[str, pygame.Surface] = {}
    images_routing: dict[str, pygame.Surface] = {}
    images_tutorials: dict[str, pygame.Surface] = {}
    images_store: dict[str, pygame.Surface] = {}
    # NPCS
    portrait_frames: dict[str, [list[pygame.Surface]]] = {}
    # Character creation
    # skin_tone/action/direction/frames
    bodies: dict[int, dict[str, list[pygame.Surface]]] = {}
    # eye_color/action/direction/frames
    eyes: dict[int, dict[str, list[pygame.Surface]]] = {}
    # hairstyle/color/action/direction/frames
    hairstyles: dict[int, dict[int, dict[str, list[pygame.Surface]]]] = {}
    # outfit/color/action/direction/frames
    outfits: dict[int, dict[int, dict[str, list[pygame.Surface]]]] = {}
    # portrait
    bodies_portrait: dict[int, dict[str, list[pygame.Surface]]] = {}
    eyes_portrait: dict[int, dict[str, list[pygame.Surface]]] = {}
    hairstyles_portrait: dict[int, dict[int, dict[str, list[pygame.Surface]]]] = {}
    routing_tutorial: dict[str, pygame.Surface] = {}
    cables_tutorial: dict[str, pygame.Surface] = {}
    subnetting_tutorial: dict[str, pygame.Surface] = {}
    all_tutorials: dict[str, dict[str, pygame.Surface]] = {}

    @classmethod
    def prepare(cls) -> None:
        """
        Preloads light resources before the heavy load, in order to improve performance.
        :return: None
        """
        cls.cursors = load_cursors(CURSORS)
        cls.fonts = load_fonts(FONTS)
        cls.images_misc = load_image_directory(IMAGES_MISC)
        cls.load_animations()

    @classmethod
    def load(cls, event: threading.Event) -> None:
        cls.images_main_menu = load_image_directory(IMAGES_MAIN_MENU)
        cls.images_selector = load_image_directory(IMAGES_SELECTOR)
        cls.images_cables = load_image_directory(IMAGES_CABLES)
        cls.images_subnetting = load_image_directory(IMAGES_SUBNETTING)
        cls.images_character_creation = load_image_directory(IMAGES_CHARACTER_CREATION)
        cls.images_actors = load_image_directory(IMAGES_ACTORS)
        cls.images_world = load_image_directory(IMAGES_WORLD)
        cls.images_book = load_image_directory(IMAGES_BOOK)
        cls.images_routing = load_image_directory(IMAGES_ROUTING)
        cls.images_tutorials = load_image_directory(IMAGES_TUTORIALS)
        cls.images_store = load_image_directory(IMAGES_STORE)
        cls.load_sounds()
        cls.load_music_paths()
        cls.load_portraits()
        cls.routing_tutorial = load_image_directory("assets/tutorials/routing")
        cls.cables_tutorial = load_image_directory("assets/tutorials/cables")
        cls.subnetting_tutorial = load_image_directory("assets/tutorials/subnetting")
        cls.all_tutorials = {"cables": cls.cables_tutorial,
                             "subnetting": cls.subnetting_tutorial,
                             "routing": cls.routing_tutorial}
        event.clear()

    @classmethod
    def load_animations(cls):
        for folder in listdir(ANIMATIONS):
            cls.animations[folder] = {}
            for animation in listdir(f"{ANIMATIONS}/{folder}"):
                cls.animations[folder][animation] = Loader.load_animation(f"{ANIMATIONS}/{folder}/{animation}")

    @classmethod
    def load_portraits(cls):
        for file in listdir(NPC_PORTRAITS):
            npc_name = file.split(".")[0].split("_")[0]
            cls.portrait_frames[npc_name] = Loader.load_portrait_frames(f"{NPC_PORTRAITS}/{file}", 96)

    @classmethod
    def load_sounds(cls):
        for folder in listdir(Paths.SOUNDS_FOLDER):
            cls.sounds[folder] = []
            for sound in listdir(f"{Paths.SOUNDS_FOLDER}/{folder}"):
                cls.sounds[folder].append(Loader.load_sound(f"{Paths.SOUNDS_FOLDER}/{folder}/{sound}"))

    @classmethod
    def load_music_paths(cls):
        for song in listdir(Paths.MUSIC_FOLDER):
            name = song.split(".")[0]
            cls.music[name] = f"{Paths.MUSIC_FOLDER}/{song}"

    @classmethod
    def load_portrait_assets(cls):
        body_path = "assets/portrait_generator/bodies"
        eyes_path = "assets/portrait_generator/eyes"
        hair_styles_path = "assets/portrait_generator/hairstyles"

        for file in listdir(body_path):
            body_type = int(file.split(".")[0].split("_")[1])
            cls.bodies_portrait[body_type] = Loader.load_portrait_frames(f"{body_path}/{file}", 64)

        for file in listdir(eyes_path):
            eyes_type = int(file.split(".")[0].split("_")[1])
            cls.eyes_portrait[eyes_type] = Loader.load_portrait_frames(f"{eyes_path}/{file}", 64)

        for file in listdir(hair_styles_path):
            variation = int(file.split("_")[1])
            color = int(file.split("_")[2].split(".")[0])
            if variation not in cls.hairstyles_portrait:
                cls.hairstyles_portrait[variation] = {}
            cls.hairstyles_portrait[variation][color] = Loader.load_portrait_frames(f"{hair_styles_path}/{file}", 64)

    @classmethod
    def load_character_creation_assets(cls, event: threading.Event):
        pygame.display.init()

        def load_bodies():
            cls.bodies = import_category_animations("bodies")

        def load_eyes():
            cls.eyes = import_category_animations("eyes")

        def load_hairstyles():
            cls.hairstyles = import_category_animations("hairstyles")

        def load_outfits():
            cls.outfits = import_category_animations("outfits")

        bodies_thread = Thread(target=load_bodies)
        eyes_thread = Thread(target=load_eyes)
        hairstyles_thread = Thread(target=load_hairstyles)
        outfits_thread = Thread(target=load_outfits)
        # portraits_thread = Thread(target=cls.load_portrait_assets())

        bodies_thread.start()
        eyes_thread.start()
        hairstyles_thread.start()
        outfits_thread.start()
        # portraits_thread.start()

        bodies_thread.join()
        eyes_thread.join()
        hairstyles_thread.join()
        outfits_thread.join()
        # portraits_thread.join()

        event.clear()
