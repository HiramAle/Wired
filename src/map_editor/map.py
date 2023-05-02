import pygame
import pytmx


class Map:
    def __init__(self, filename: str):
        self.data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight
        self.layers = [layer for layer in self.data.layers if
                       isinstance(layer, (pytmx.TiledTileLayer, pytmx.TiledObjectGroup))]

    def render(self, surface: pygame.Surface):
        ...
