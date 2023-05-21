import pygame

def dibujar_contorno_imagen(image_path, separation):
    # Inicializar pygame
    pygame.init()

    # Crear la ventana
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dibujar contorno de imagen")

    # Cargar la imagen
    image = pygame.image.load(image_path)

    # Obtener el rectángulo que representa la imagen
    image_rect = image.get_rect()

    # Crear un rectángulo más grande para el contorno separado
    contour_rect = image_rect.inflate(separation * 2, separation * 2)

    # Obtener el centro del rectángulo del contorno
    contour_center = contour_rect.center

    # Dibujar la imagen en el centro de la pantalla
    screen.blit(image, image_rect)

    # Dibujar el contorno como un rectángulo en la posición correcta
    pygame.draw.rect(screen, (0, 0, 0), contour_rect, 1)

    # Dibujar líneas desde las esquinas del contorno al centro de la imagen
    pygame.draw.line(screen, (0, 0, 0), contour_rect.topleft, contour_center)
    pygame.draw.line(screen, (0, 0, 0), contour_rect.topright, contour_center)
    pygame.draw.line(screen, (0, 0, 0), contour_rect.bottomleft, contour_center)
    pygame.draw.line(screen, (0, 0, 0), contour_rect.bottomright, contour_center)

    # Actualizar la pantalla
    pygame.display.flip()

    # Esperar a que se cierre la ventana
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Finalizar pygame
    pygame.quit()

# Ejemplo de uso
dibujar_contorno_imagen("../../assets/images/misc/notification.png", 10)
