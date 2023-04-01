import pygame
from json import dumps, load
from src.utils.image import load_sprite_sheet
from os.path import isdir
from os import listdir
from src.gui.font import Font


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
    image.set_colorkey(color_key)
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
