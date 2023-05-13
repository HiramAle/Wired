import pygame
import os
from enum import Enum
from engine.constants import Constants
from engine.loader import Loader


class AssetsManager:
    class Assets(Enum):
        CURSORS = 0

    def __init__(self):
        self.cursors: dict[str, pygame.cursors.Cursor] = {}

    def load_cursors(self):
        for file in os.listdir(Constants.Paths.CURSORS):
            name = file.split(".")[0]
            self.cursors[name] = Loader.load_cursor(file)
