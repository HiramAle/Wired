import pygame.mixer
from engine.preferences import Preferences


class AudioManager:
    channels = []

    @classmethod
    def init(cls):
        cls.channels = []
        pygame.mixer.init()

    @staticmethod
    def set_volume(volume: int):
        if 0 > volume > 20:
            raise ValueError("Volume cannot be greater than 20 and lesser than 0.")
        Preferences.volume = volume * 5
        Preferences.save()
