import pygame
import pytmx
from src.game_object.sprite import Sprite


class Obstacle(Sprite):
    def __init__(self, position: tuple, width, height, *groups, **kwargs):
        super().__init__("map_obstacle", (position[0] * 2, position[1] * 2), pygame.Surface((width * 2, height * 2)),
                         *groups, **kwargs)
        self.layer = 5
        self.centered = False


class Tile(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, *groups, **kwargs):
        super().__init__("tile", (position[0], position[1]), image, *groups, **kwargs)
        self.centered = False


class Object(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, *groups, **kwargs):
        super().__init__("object", (position[0], position[1]), image, *groups, **kwargs)
        self.x += self.rect.width / 2
        self.y += self.rect.height / 2


class TiledMap:
    def __init__(self, data: pytmx.TiledMap):
        # Map data
        self.tmx_data = data
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.get_by_gid = self.tmx_data.get_tile_image_by_gid

        self.background = pygame.Surface((self.width, self.height))
        self.background.set_colorkey((0, 0, 0))
        self.dynamic: list[Tile] = []
        self.objects: list[Object] = []

        self.load()
        # for tile_object in self.tmx_data.objects:
        #     self.obstacles.append(Obstacle((tile_object.x, tile_object.y), tile_object.width, tile_object.height))
        #
        # layer1: pytmx.TiledTileLayer = self.tmx_data.get_layer_by_name("muebles")
        # layer2: pytmx.TiledTileLayer = self.tmx_data.get_layer_by_name("toppers")
        #
        # for x, y, tile in layer1.tiles():
        #     self.furniture.append(Tile((x * self.tile_width, y * self.tile_height), tile))
        #
        # for x, y, tile in layer2.tiles():
        #     self.furniture.append(Tile((x * self.tile_width, y * self.tile_height), tile, layer=3))

    def load(self):
        for layer in self.tmx_data.visible_layers:
            if self.get_layer_class(layer) == "static":
                for x, y, gid in layer:
                    tile = self.get_by_gid(gid)
                    if tile:
                        self.background.blit(tile, (x * self.tile_width, y * self.tile_height))
        for x, y, tile in self.tmx_data.get_layer_by_name("furniture").tiles():
            self.dynamic.append(Tile((x * self.tile_width, y * self.tile_height), tile))

        for tiled_object in self.tmx_data.objects:
            if not tiled_object.image:
                continue
            self.objects.append(Object((tiled_object.x, tiled_object.y), tiled_object.image))

    @staticmethod
    def get_layer_class(layer: pytmx.TiledTileLayer) -> str:
        try:
            return layer.__getattribute__("class")
        except AttributeError:
            return ""

    # def render(self, display: pygame.Surface):
    #     for layer in self.tmx_data.visible_layers:
    #         if isinstance(layer, pytmx.TiledTileLayer):
    #             for x, y, gid in layer:
    #                 tile = self.get_by_gid(gid)
    #                 if tile:
    #                     display.blit(tile, (x * self.tile_width, y * self.tile_height))

    def make_map(self) -> pygame.Surface:
        map_surface = pygame.Surface((self.width, self.height))
        self.render(map_surface)
        return map_surface
