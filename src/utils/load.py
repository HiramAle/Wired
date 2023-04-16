import enum
import os.path

import pygame
import time
from json import dumps, load
from src.utils.image import load_sprite_sheet
from os.path import isdir
from os import listdir
from src.gui.font import Font
from src.constants.paths import *


def load_json(path: str) -> dict:
    """
    Get the data from a JSON file into a dict.
    :param path: Path from the JSON file.
    :return: Dictionary containing the JSON file data.
    """
    with open(path, "r") as json_file:
        data = load(json_file)
    return data


def write_json(path: str, data: dict):
    """
    Write a dictionary into a JSON file.
    :param path: Path from the JSON file.
    :param data: Dictionary to save into the JSON file.
    """
    with open(path, "w") as json_file:
        json_file.write(dumps(data))


def load_image(path: str, color_key=(0, 0, 0)) -> pygame.Surface:
    """
    Load an image from the given path and set the color key to the specified color.
    :param path: The path of the image file.
    :param color_key: The color to use as the transparent color in the image.
    :return: A Pygame Surface object representing the loaded image.
    """

    image = pygame.image.load(path).convert_alpha()
    # image.set_colorkey(color_key)

    # new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    # new_image.blit(image, (0, 0))
    return image


def load_image_directory(path: str) -> dict:
    """
    Load a directory of images into a dictionary.
    Recursively searches subdirectories.
    :param path: The path of the directory to load.
    :return: A dictionary mapping file names to Pygame Surfaces.
    """
    data = {}
    for file in listdir(path):
        file_path = f"{path}/{file}"
        if isdir(file_path):
            data[file] = load_image_directory(file_path)
        else:
            name = file.split(".")[0]
            data[name] = load_image(file_path)
    return data


def load_cursors(path: str) -> dict[str, pygame.cursors.Cursor]:
    """
    Load a directory of cursor images and return them as a dictionary of pygame Cursor objects.
    :param path: The path to the directory containing the cursor images.
    :return: A dictionary of pygame Cursor objects, keyed by the filename of the corresponding image file.
    """
    return {name: pygame.cursors.Cursor((0, 0), pygame.transform.scale_by(image, 3))
            for name, image in load_image_directory(path).items()}


def load_fonts(path: str) -> dict[str, Font]:
    fonts = {}
    for font_file in listdir(path):
        file_path = f"{path}/{font_file}"
        font_name = font_file.split(".")[0]
        fonts[font_name] = Font(font_name, file_path)
    return fonts


def load_animation(path: str) -> tuple[pygame.Surface, dict]:
    data = None
    sprite_sheet = None
    for file in listdir(path):
        if file.endswith(".json"):
            data = load_json(f"{path}/data.json")
        else:
            sprite_sheet = load_image(f"{path}/{file}")
    return sprite_sheet, data


def load_animations(path: str) -> dict[str, dict[str, list]]:
    animations = {}
    for folder in listdir(path):
        folder_path = f"{path}/{folder}"
        animations[folder] = {}
        for animation in listdir(folder_path):
            animation_path = f"{folder_path}/{animation}"
            sprite_sheet, data = load_animation(animation_path)
            frames = load_sprite_sheet(sprite_sheet, data)
            animations[folder][animation] = frames, data

    return animations


def export_animation_frames(sprite_sheet: pygame.Surface) -> dict:
    sprite_height = 48
    sprite_width = 32
    crop_height = 64
    crop_width = 32
    animation_frames = load_json(DATA_CHARACTER_CREATION_FRAMES)
    animations = {action: {direction: [] for direction in value.keys()} for action, value in animation_frames.items()}
    row = 0
    column = 0
    for animation, directions in animation_frames.items():
        for direction, frames in directions.items():
            for frame in range(frames):
                x_crop = column * crop_width
                y_crop = 16 + (row * crop_height)
                image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x_crop, y_crop, crop_width, crop_height))
                animations[animation][direction].append(image)
                column += 1
        row += 1
        column = 0
    return animations


def crop_image(image: pygame.Surface, x_crop: int, y_crop: int, crop_width: int, crop_height: int) -> pygame.Surface:
    """
    Load a directory of cursor images and return them as a dictionary of pygame Cursor objects.
    :param image: Source image to crop.
    :param x_crop:
    :param y_crop:
    :param crop_width:
    :param crop_height:
    :return: The image cropped.
    """
    crop_rect = pygame.Rect(x_crop, y_crop, crop_width, crop_height)
    new_image = pygame.Surface(crop_rect.size, pygame.SRCALPHA)
    new_image.blit(image, (0, 0), crop_rect)
    return new_image


def get_idle_frames(category: str):
    ...


# Load animation data
animation_data = load_json(DATA_CHARACTER_CREATION_FRAMES)


def get_animation_by_name(sprite_sheet: pygame.Surface, name: str) -> dict[str, list]:
    # Get the index of the animation
    animation_index = list(animation_data.keys()).index(name)
    # Set the directions based on the animation
    directions: dict = animation_data.get(name, {})
    # Fill directory with empty lists
    animation_frames: dict[str, list] = {direction: [] for direction in directions.keys()}

    sprite_index = 0
    for direction, frames in directions.items():
        for frame in range(frames):
            x_crop = sprite_index * 32
            y_crop = 64 * animation_index
            animation_frames[direction].append(crop_image(sprite_sheet, x_crop, y_crop, 32, 64))
            sprite_index += 1

    return animation_frames


paths = {
    "bodies": BODIES,
    "eyes": EYES,
    "hairstyles": HAIRSTYLES,
    "outfits": OUTFITS
}


def import_category_animations(category: str) -> dict[int, dict]:
    path = paths.get(category)
    category_animations: dict[int, dict] = {}
    for filename in listdir(path):
        sprite_sheet = pygame.image.load(f"{path}/{filename}").convert_alpha()

        if category in ["bodies", "eyes"]:
            color = int(filename.split("_")[1].split(".")[0])
            category_animations[color] = get_animation_by_name(sprite_sheet, "idle")

        elif category in ["hairstyles", "outfits"]:
            variation = int(filename.split("_")[1])
            color = int(filename.split("_")[2].split(".")[0])

            if variation not in category_animations:
                category_animations[variation] = {}

            category_animations[variation][color] = get_animation_by_name(sprite_sheet, "idle")

    return category_animations


def save_sprite_sheet(body: int, eyes: int, hairstyle: tuple[int, int], outfit: tuple[int, int]):
    body_path = f"{BODIES}/body_{body}.png"
    eyes_path = f"{EYES}/eyes_{eyes}.png"
    hairstyle_path = f"{HAIRSTYLES}/hairstyle_{hairstyle[0]}_{hairstyle[1]}.png"
    outfit_path = f"{OUTFITS}/outfit_{outfit[0]}_{outfit[1]}.png"

    try:
        body_image = load_image(body_path)
        eyes_image = load_image(eyes_path)
        hairstyle_image = load_image(hairstyle_path)
        outfit_image = load_image(outfit_path)
    except FileNotFoundError:
        print("File Not Found")
    else:
        sprite_sheet = pygame.Surface(body_image.get_size(), pygame.SRCALPHA)

        sprite_sheet.blit(body_image, (0, 0))
        sprite_sheet.blit(outfit_image, (0, 0))
        sprite_sheet.blit(hairstyle_image, (0, 0))
        sprite_sheet.blit(eyes_image, (0, 0))

        pygame.image.save(sprite_sheet, f"{USER_DATA}/sprite_sheet.png")


def import_character_generator():
    paths = {
        "bodies": BODIES,
        "eyes": EYES,
        "hairstyles": HAIRSTYLES,
        "outfits": OUTFITS
    }
    files = {category: {} for category in paths.keys()}

    for option, path in paths.items():
        for filename in sorted(listdir(path)):
            if option in ["bodies", "eyes"]:
                color = filename.split("_")[1].split(".")[0]
                sprite_sheet = pygame.image.load(f"{path}/{filename}").convert_alpha()
                files[option][color] = export_animation_frames(sprite_sheet)

            elif option in ["hairstyles", "outfits"]:
                type = filename.split("_")[1]
                color = filename.split("_")[2].split(".")[0]
                if type not in files[option]:
                    files[option][type] = {}
                sprite_sheet = pygame.image.load(f"{path}/{filename}").convert_alpha()
                files[option][type][color] = export_animation_frames(sprite_sheet)

    return files
