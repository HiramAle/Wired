import pygame
from engine.loader import Loader


def get_animation_frames(filename: str, data: dict) -> list[pygame.Surface]:
    sprite_sheet = Loader.load_image(filename)
    frames = []
    for row in range(data.get("height", 0)):
        for column in range(data.get("width", 0)):
            x = column * 
