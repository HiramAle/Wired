import pygame.mixer

import src.user.preferences as preferences


class AudioManager:
    channels = []

    @classmethod
    def init(cls):
        cls.channels = []
        pygame.mixer.init()

    @staticmethod
    def set_volume(volume: int):
        if 0 > volume > 5:
            raise ValueError("Volume cannot be greater than 5 and lesser than 0.")
        preferences.volume = volume
        preferences.set_preferences({"volume": volume})
