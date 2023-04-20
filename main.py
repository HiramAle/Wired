import threading
import time

import pygame
import src.engine.window as window
import src.engine.input as input
import src.engine.time as game_time
import src.user.preferences as preferences
import src.user.saves as saves
import src.engine.assets as assets
import src.scene.core.scene_manager as scene_manager
import src.engine.data as data


class Game:
    def __init__(self):
        pygame.init()
        data.init()
        assets.prepare()
        preferences.init()
        saves.init()
        window.init()
        scene_manager.init()

    def run(self):
        while True:
            input.update()

            # update = threading.Thread(target=scene_manager.update)
            # render = threading.Thread(target=scene_manager.render)

            # update.start()
            # render.start()

            # update.join()
            # render.join()

            scene_manager.update()
            scene_manager.render()

            game_time.update()
            window.update()


if __name__ == '__main__':
    Game().run()
