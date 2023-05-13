import pygame.mixer
from random import choice
from engine.preferences import Preferences
from engine.assets import Assets


class AudioManager:

    @classmethod
    def init(cls):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

    @classmethod
    def play_music(cls, name: str):
        song = Assets.music.get(name, None)
        if not song:
            print("Song not found")
            return
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(Preferences.volume / 250)

    @classmethod
    def play_sound(cls, sound: pygame.mixer.Sound):
        sound.set_volume(Preferences.volume / 250)
        sound.play()

    @classmethod
    def play_random_from(cls, name: str):
        cls.play_sound(choice(Assets.sounds[name]))

    @staticmethod
    def set_volume(volume: int):
        if 0 > volume > 20:
            raise ValueError("Volume cannot be greater than 20 and lesser than 0.")
        Preferences.volume = volume * 5
        pygame.mixer.music.set_volume(Preferences.volume / 250)
        Preferences.save()
