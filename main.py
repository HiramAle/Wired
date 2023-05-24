import time

import pygame
# New Imports
from engine.preferences import Preferences
from engine.window import Window
from engine.data import Data
from engine.input import Input
from engine.time import Time
from engine.assets import Assets
from engine.scene.scene_manager import SceneManager
from engine.save_manager import instance as save_manager
from engine.item_manager import ItemManager
from src.scenes.world.tasks import TaskManager


class Game:
    def __init__(self):
        pygame.init()
        ItemManager.load_items()
        TaskManager.load_tasks()
        Data.init()
        Preferences.load()
        save_manager.load()
        Window.init()
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
