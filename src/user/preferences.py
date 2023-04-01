import pygame.display
from src.constants.paths import PREFERENCES, DEFAULT_PREFERENCES
from src.utils.load import load_json, write_json

window_width = 0
window_height = 0
sounds = 0
music = 0


def init() -> None:
    """
    Initialization method for preferences handler
    """
    global window_width, window_height, sounds, music
    try:
        preferences = load_json(PREFERENCES)
    except FileNotFoundError:
        display_data = pygame.display.Info()
        preferences = load_json(DEFAULT_PREFERENCES)
        preferences["window_width"] = display_data.current_w
        preferences["window_height"] = display_data.current_h
        write_json(PREFERENCES, preferences)

    update(preferences)


def set_preferences(data: dict) -> None:
    """
    Set some preferences to a determinate value.
    :param data: Dictionary containing the new values for preferences.
    """
    preferences = load_json(PREFERENCES)
    for key, value in data.items():
        preferences[key] = value
    write_json(PREFERENCES, preferences)
    update(preferences)


def update(preferences: dict) -> None:
    """
    Update the variables values of the preferences.
    :param preferences: New preferences values.
    """
    global window_width, window_height, sounds, music
    window_width = preferences["window_width"]
    window_height = preferences["window_height"]
    sounds = preferences["sounds"]
    music = preferences["music"]
