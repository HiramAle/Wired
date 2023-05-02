import pygame
from sys import exit

from src.test.singleton.preferences import instance as preferences

from src.test.singleton.window import instance as window


class Game:
    def __init__(self):
        pygame.init()
        preferences.load()
        window.init()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


if __name__ == '__main__':
    Game().run()
