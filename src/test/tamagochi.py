import pygame
import time
import random

pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tamaño de la pantalla
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Fuentes
FONT_SMALL = pygame.font.Font(None, 25)
FONT_LARGE = pygame.font.Font(None, 50)

# Tiempo
clock = pygame.time.Clock()

class Tamagotchi():
    def __init__(self):
        self.hunger = 50
        self.happiness = 50
        self.health = 50

    def feed(self):
        self.hunger -= 10
        self.happiness += 5

    def play(self):
        self.happiness += 10
        self.health += 5

    def sleep(self):
        self.health += 10

def game_loop():
    # Crear pantalla
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Tamagotchi")

    # Crear Tamagotchi
    tamagotchi = Tamagotchi()

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    tamagotchi.feed()
                elif event.key == pygame.K_p:
                    tamagotchi.play()
                elif event.key == pygame.K_s:
                    tamagotchi.sleep()

        # Dibujar fondo
        screen.fill(WHITE)

        # Dibujar texto
        text_hunger = FONT_SMALL.render("Hunger: {}".format(tamagotchi.hunger), True, BLACK)
        screen.blit(text_hunger, [10, 10])

        text_happiness = FONT_SMALL.render("Happiness: {}".format(tamagotchi.happiness), True, BLACK)
        screen.blit(text_happiness, [10, 40])

        text_health = FONT_SMALL.render("Health: {}".format(tamagotchi.health), True, BLACK)
        screen.blit(text_health, [10, 70])

        # Dibujar Tamagotchi
        tamagotchi_image = pygame.Surface((30,30))
        tamagotchi_image.fill("RED")
        tamagotchi_image.set_colorkey(WHITE)
        screen.blit(tamagotchi_image, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100])

        # Actualizar pantalla
        pygame.display.flip()

        # Esperar un poco antes de actualizar de nuevo
        clock.tick(10)

game_loop()
pygame.quit()
