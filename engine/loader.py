import json
import pygame
from engine.animation.animation import Animation
from os import listdir


class Loader:
    @staticmethod
    def load_json(path: str) -> dict:
        data = {}
        try:
            with open(path, "r", encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("JSON file not found")
        finally:
            return data

    @staticmethod
    def save_json(path: str, data: dict) -> bool:
        # try:
        #
        # except:
        #     print("Unable to save JSON file")
        #     return False
        with open(path, "w") as file:
            json.dump(data, file, indent=2)
        return True

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        image = pygame.Surface((32, 32), pygame.SRCALPHA)
        try:
            image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError:
            print("Image file not found")
        finally:
            return image

    @staticmethod
    def load_sound(path: str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(path)

    @staticmethod
    def load_cursor(path: str) -> pygame.Cursor:
        return pygame.Cursor((0, 0), pygame.transform.scale_by(Loader.load_image(path), 3))

    @staticmethod
    def load_font(path: str, size: int) -> pygame.Font:
        return pygame.Font(path, size)

    @staticmethod
    def load_animation(path: str) -> Animation:
        sprite_sheet = None
        animation_data = None
        for file in listdir(path):
            if file.endswith(".png"):
                sprite_sheet = Loader.load_image(f"{path}/{file}")
            elif file.endswith(".json"):
                animation_data = Loader.load_json(f"{path}/{file}")
        if not sprite_sheet and not animation_data:
            assert "Sprite sheet or JSON file not found in folder"
        return Animation(sprite_sheet, animation_data)
