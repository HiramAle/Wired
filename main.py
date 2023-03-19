import pygame
import src.engine.window as window
import src.engine.input as input
import src.engine.time as time
import src.user.preferences as preferences
import src.engine.assets as assets


class Game:
    def __init__(self):
        pygame.init()
        assets.prepare()
        preferences.init()
        window.init()

    @staticmethod
    def run():
        while True:
            input.update()
            time.update()
            window.update()


if __name__ == '__main__':
    Game().run()
