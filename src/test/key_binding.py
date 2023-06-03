import sys

import pygame

pygame.init()
pygame.display.set_mode((50, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(event.key)
    pygame.display.update()

