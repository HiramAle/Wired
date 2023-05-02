import sys
import pygame
from src.map_editor.map import Map


class Layer:
    def __init__(self, name: str, position: tuple, visible: int):
        self.name = name
        self.position = pygame.Vector2(position)
        self.image = font.render(name, False, "white")
        self.visible = bool(visible)
        self.selected = False
        self.visible_button = pygame.Surface((10, 10))
        self.visible_button.fill("blue")

    @property
    def rect_button(self):
        return self.visible_button.get_rect(center=(self.position.x + self.rect.right + 10, self.rect.centery))

    @property
    def rect(self):
        return self.image.get_rect(topleft=self.position)

    def render(self, surface: pygame.Surface, offset: pygame.Vector2):
        rect = self.rect
        rect.x += offset.x
        rect.y += offset.y
        if self.selected:
            pygame.draw.rect(surface, "gray", rect)
        surface.blit(self.image, rect)
        btn_rect = self.rect_button
        btn_rect.x += offset.x
        btn_rect.y += offset.y
        surface.blit(self.visible_button, btn_rect)


pygame.init()
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Map editor")
canvas = pygame.Surface((640, 320))
clock = pygame.time.Clock()
dt = 0.2
mouse = pygame.math.Vector2(0, 0)

scroll_offset = pygame.Vector2(0, 0)

font = pygame.Font("../../assets/fonts/monogram.ttf", 16)
tiled_map = Map("../../data/maps/TMX/Village.tmx")

layers = []
selected_layer: Layer | None = None

for index, layer in enumerate(tiled_map.layers):
    layers.append(Layer(layer.name, (10, 10 + (index * 20)), layer.visible))

while True:
    for event in pygame.event.get():
        event: pygame.Event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                scroll_offset.y += 5
            else:
                scroll_offset.y -= 5

        for layer in layers:
            if layer.rect.collidepoint(mouse - scroll_offset) and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(f"{layer.name} clicked")
                    for layer2 in layers:
                        layer2.selected = False
                    layer.selected = True
                    selected_layer = layer
                break

    mouse.x = int(pygame.mouse.get_pos()[0] / 1280 * 640)
    mouse.y = int(pygame.mouse.get_pos()[1] / 720 * 320)

    canvas.fill("#2e2e2e")

    for layer in layers:
        layer.render(canvas, scroll_offset)

    window.blit(pygame.transform.scale(canvas, (1280, 720)), (0, 0))

    pygame.display.update()
    dt = clock.tick() / 1000
