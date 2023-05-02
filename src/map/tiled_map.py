import pygame
import pytmx
from src.game_object.sprite import Sprite


class Obstacle(Sprite):
    def __init__(self, position: tuple, width, height, *groups, **kwargs):
        super().__init__("map_obstacle", position, pygame.Surface((width, height)), *groups, **kwargs)
        self.layer = 5
        self.centered = False


class Tile(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, *groups, **kwargs):
        super().__init__("tile", (position[0], position[1]), image, *groups, **kwargs)
        self.centered = False


class NPCSpawn(Sprite):
    def __init__(self, name: str, position: tuple, *groups, **kwargs):
        super().__init__(name, (position[0], position[1]), pygame.Surface((0, 0)), *groups, **kwargs)
        self.x += self.rect.width / 2
        self.y += self.rect.height / 2


class Object(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, layer: int, *groups, **kwargs):
        super().__init__("object", (position[0], position[1]), image, *groups, **kwargs)
        self.layer = layer
        self.x += self.rect.width / 2
        self.y += self.rect.height / 2

    def __repr__(self):
        return f"{self.name} {self.position} {self.layer}"


class Trigger(Sprite):
    def __init__(self, name: str, position: tuple, width: float, height: float):
        super().__init__(name, position, pygame.Surface((width, height)))
        self.x += self.rect.width / 2
        self.y += self.rect.height / 2

    def on_enter(self, *args, **kwargs):
        if self.name == "stairs":
            kwargs["player"].speed = 100

        print("enter", self.name)

    def on_exit(self, *args, **kwargs):
        if self.name == "stairs":
            kwargs["player"].speed = 150
        print("exit", self.name)


class TiledMap:
    def __init__(self, data: pytmx.TiledMap):
        # Map data
        self.tmx_data = data
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.get_by_gid = self.tmx_data.get_tile_image_by_gid
        self.player_position = 0, 0
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.objects: list[Object] = []
        self.collisions: list[Obstacle] = []
        self.interactions: list[Trigger] = []
        self.npcs: list[NPCSpawn] = []

        self.load()

    def load(self):
        for layer in self.tmx_data.visible_layers:
            try:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        tile = self.get_by_gid(gid)
                        if tile:
                            self.background.blit(tile, (x * self.tile_width, y * self.tile_height))
            except TypeError:
                continue

        for index, object_layer in enumerate(reversed([layer for layer in self.tmx_data.objectgroups])):
            for tiled_object in object_layer:
                tiled_object: pytmx.TiledObject
                # print(f"{object_layer.name} {tiled_object.image}")
                if tiled_object.image:

                    self.objects.append(Object((tiled_object.x, tiled_object.y), tiled_object.image, index))
                else:
                    if tiled_object.name:
                        if tiled_object.name == "player_":
                            self.player_position = tiled_object.x, tiled_object.y
                        elif tiled_object.name == "player_village" and self.player_position == (0, 0):
                            self.player_position = tiled_object.x, tiled_object.y
                        elif object_layer.name == "interactions":
                            self.interactions.append(
                                Trigger(tiled_object.name, (tiled_object.x, tiled_object.y), tiled_object.width,
                                        tiled_object.height))
                        elif tiled_object.type == "npc_spawn":
                            self.npcs.append(NPCSpawn(tiled_object.name, (tiled_object.x, tiled_object.y)))
                    else:
                        self.collisions.append(
                            Obstacle((tiled_object.x, tiled_object.y), tiled_object.width, tiled_object.height))
        self.objects.sort(key=lambda obj: obj.y)

    @staticmethod
    def get_layer_class(layer: pytmx.TiledTileLayer) -> str:
        try:
            return layer.__getattribute__("class")
        except AttributeError:
            return ""
