import pygame
import random

# Define algunas constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLANET_SIZE = 30
PLANET_COUNT = 10

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Generación de Planetas")

# Define una lista para almacenar los planetas generados
planets = []

# Genera los planetas
for i in range(PLANET_COUNT):
    # Genera las coordenadas del planeta de manera aleatoria
    x = random.randint(0, SCREEN_WIDTH - PLANET_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - PLANET_SIZE)
    # Determina si el planeta alberga vida
    has_life = random.random() < 0.5
    # Agrega el planeta a la lista
    planets.append((x, y, has_life, f"Planeta {i + 1}"))

# Bucle principal del juego
while True:
    # Maneja eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Dibuja los planetas en la pantalla
    screen.fill((0, 0, 0))  # Borra la pantalla
    for planet in planets:
        # Dibuja el planeta como un círculo
        planet_rect = pygame.draw.circle(screen, (255, 255, 255), (planet[0], planet[1]), PLANET_SIZE)
        # Verifica si el mouse está sobre el planeta y muestra la información si es así
        mouse_pos = pygame.mouse.get_pos()
        if planet_rect.collidepoint(mouse_pos):
            info_font = pygame.font.Font(None, 20)
            info_text = f"Planeta: {planet[3]}"
            if planet[2]:
                info_text += " (con vida)"
            info_surface = info_font.render(info_text, True, "green")
            screen.blit(info_surface, (10, 10))

    pygame.display.flip()  # Actualiza la pantalla
