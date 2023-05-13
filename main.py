import pygame
# New Imports
from engine.preferences import Preferences
from engine.window import Window
from engine.data import Data
from engine.input import Input
from engine.time import Time
from engine.assets import Assets
from engine.scene.scene_manager import SceneManager


class Game:
    def __init__(self):
        pygame.init()
        Preferences.load()
        Window.init()
        Data.init()
        Assets.prepare()
        SceneManager.init()

    @staticmethod
    def run():
        while True:
            Input.update()
            SceneManager.update()
            SceneManager.render()
            Time.update()
            Window.update()


if __name__ == '__main__':
    Game().run()
