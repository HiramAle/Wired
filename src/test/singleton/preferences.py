import json
import pygame
from ctypes import windll
from os import environ

# Deactivate Windows DPI escalation
windll.user32.SetProcessDPIAware()
# Set the window centered on screen
environ['SDL_VIDEO_CENTERED'] = "1"


class Preferences:
    def __init__(self):
        self.path = "preferences.json"
        self.window_width = 0
        self.window_height = 0
        self.fullscreen = True
        self.borderless = False
        self.windowed = False
        self.volume = 10

    def data(self) -> dict:
        return {"window_width": self.window_width,
                "window_height": self.window_height,
                "fullscreen": self.fullscreen,
                "borderless": self.borderless,
                "windowed": self.windowed,
                "volume": self.volume}

    def load(self):
        try:
            with open(self.path, "r") as prefs:
                data = json.load(prefs)
            self.window_width = data["window_width"]
            self.window_height = data["window_height"]
            self.fullscreen = data["fullscreen"]
            self.borderless = data["borderless"]
            self.windowed = data["windowed"]
            self.volume = data["volume"]
            print("Preferences loaded.")
        except FileNotFoundError:
            print("Unable to lad preferences, making new preferences file.")
            self.window_width, self.window_height = pygame.display.get_desktop_sizes()[0]
            self.save()

    def save(self):
        with open(self.path, "w") as prefs:
            json.dump(self.data(), prefs, indent=2)
        print("Preferences saved.")


instance = Preferences()
