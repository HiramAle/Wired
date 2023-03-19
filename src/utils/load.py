import pygame
from json import dumps, load
from os.path import exists, isdir, join
from os import listdir


def read_json(path: str) -> dict:
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


def load_cursor(path: str) -> dict[str, pygame.cursors.Cursor]:
    """
    Load a directory of cursor images and return them as a dictionary of pygame Cursor objects.
    :param path: The path to the directory containing the cursor images.
    :return: A dictionary of pygame Cursor objects, keyed by the filename of the corresponding image file.
    """
    return {name: pygame.cursors.Cursor((0, 0), pygame.transform.scale_by(image, 3))
            for name, image in load_image_directory(path).items()}
