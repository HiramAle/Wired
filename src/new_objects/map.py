import math
import sys
import pygame
import pytmx
from src.new_objects.entity import Entity, Group
from src.new_objects.entities import Tile, Obstacle


def get_layer_class(layer: pytmx.TiledTileLayer | pytmx.TiledObjectGroup) -> str:
    try:
        return layer.__getattribute__("class")
    except AttributeError:
        return ""


class Map:
    def __init__(self, filename: str):
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.get_by_gid = self.tmx_data.get_tile_image_by_gid
        self.tile_size = 32
        self.tile_scale = 1

        self.obstacles: list[Obstacle] = []
        self.objects: list[Tile] = []

        for layer in self.tmx_data.layers:
            layer: pytmx.TiledTileLayer | pytmx.TiledObjectGroup
            if layer.__class__.__name__ == "TiledGroupLayer":
                continue
            # Create background

            if get_layer_class(layer) == "static":
                for x, y, gid in layer:
                    tile = self.get_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale_by(tile, self.tile_scale)
                        self.background.blit(tile, (x * self.tile_size, y * self.tile_size))
            elif get_layer_class(layer) == "dinamic" and isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.get_by_gid(gid)
                    tile: pygame.Surface
                    if tile:
                        tile_entity = Tile()
                        tile_entity.position = x * self.tile_size, y * self.tile_size
                        tile_entity.image = pygame.transform.scale_by(tile, self.tile_scale)
                        self.objects.append(tile_entity)
            elif layer.name == "collision":
                layer: pytmx.TiledObjectGroup
                for tile_object in layer:
                    tile_object: pytmx.TiledObject
                    self.obstacles.append(
                        Obstacle(pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)))
