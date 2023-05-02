import pygame
import sys
from src.new_objects.actor import Actor

pygame.init()
display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = 0.2

actor = Actor()
actor.image = pygame.image.load("../../assets/images/misc/space_background.png")

while True:
    pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ...

    display.fill("#2e2e2e")

    actor.__position = pygame.mouse.get_pos()
    actor.render(display)
    pygame.draw.rect(display, "red", actor.collider, 2)

    pygame.display.update()
    dt = clock.tick() / 1000
