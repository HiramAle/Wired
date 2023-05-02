import sys

import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = 0.2

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Update
    # Render
    screen.fill("#2e2e2e")
    pygame.draw.rect(screen,"gray",pygame.Rect(0,36))

    pygame.display.update()
    dt = clock.tick() / 1000
