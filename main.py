import pygame
import src.engine.window as window
import src.engine.input as input
import src.engine.time as time
import src.user.preferences as preferences
import src.engine.assets as assets
import src.scene.core.scene_manager as scene_manager
import src.engine.data as data


class Game:
    def __init__(self):
        pygame.init()
        data.init()
        assets.prepare()
        preferences.init()
        window.init()
        scene_manager.init()


    @staticmethod
    def run():
        while True:
            input.update()
            scene_manager.update()
            scene_manager.render()
            time.update()
            window.update()


if __name__ == '__main__':
    Game().run()
