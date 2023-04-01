import pygame
pygame.init()
SURF_WIDTH, SURF_HEIGHT = 400, 300
surface = pygame.display.set_mode((SURF_WIDTH, SURF_HEIGHT))
pygame.display.set_caption("Layers")

class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width=50, height=20, colour="red", layer=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.rect = self.image.get_rect().move(x, y)
        self._layer = layer

layers = pygame.sprite.LayeredUpdates()
layers.add(MySprite(x=120, y=140))
layers.add(MySprite(x=160, y=140, colour="blue", layer=1))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                layers.switch_layer(0, 1)

    layers.draw(surface)
    pygame.display.update()

pygame.quit()