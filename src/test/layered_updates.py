import pygame

# Inicializar Pygame
pygame.init()

# Crear la ventana
window = pygame.display.set_mode((640, 480))


class Sprite:
    def __init__(self, surface: pygame.Surface):
        self.image = surface
        self.visible = True

    def render(self, display: pygame.Surface, x: int):
        display.blit(self.image, (x, 200))


# Cargar los sprites
sprite1 = Sprite(pygame.image.load("../../assets/images/main_menu/note_music.png"))
sprite2 = Sprite(pygame.image.load("../../assets/images/main_menu/note_music.png"))
sprite3 = Sprite(pygame.image.load("../../assets/images/main_menu/note_music.png"))
sprites = [sprite1, sprite2, sprite3]

# Índice del último sprite oculto
hidden_index = len(sprites) - 1

# Bucle principal
while True:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo
                if hidden_index >= 0:
                    sprites[hidden_index].visible = False
                    hidden_index -= 1
            elif event.button == 3:  # Botón derecho
                if hidden_index < len(sprites) - 1:
                    hidden_index += 1
                    sprites[hidden_index].visible = True

    # Dibujar los sprites
    window.fill((255, 255, 255))  # Rellenar la ventana con blanco
    for i, sprite in enumerate(sprites):
        if sprite.visible:
            sprite.render(window, 10 + (i * 20))

    # Actualizar la pantalla
    pygame.display.update()
