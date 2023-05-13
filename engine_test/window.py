import pygame
from engine.preferences import instance as preferences
from enum import Enum


class Window:
    class Cursor(Enum):
        ARROW = 0
        HAND = 1
        GRAB = 2

    def __init__(self):
        self.width = preferences.window_width
        self.height = preferences.window_height
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        self.__cursor_state = self.Cursor.ARROW

    def set_cursor(self, cursor: Cursor):
        if cursor == self.__cursor_state:
            return
        pygame.mouse.set_cursor()
