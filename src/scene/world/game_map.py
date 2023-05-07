import pytmx
import pygame
from src.scene.world.trigger import Trigger
from src.scene.world.tiled_object import TiledObject
from src.scene.world.position import Position


class GameMap:
    def __init__(self, map_data: pytmx.TiledMap):
        self.data = map_data
        # Map dimensions
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight
        self.tile_width = self.data.tilewidth
        self.tile_height = self.data.tileheight
        # Map objects
        self.ground = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.player_position = 0, 0
        self.objects_layers = [layer for layer in self.data.layers if isinstance(layer, pytmx.TiledObjectGroup)]
        self.tiled_layers = [layer for layer in self.data.layers if isinstance(layer, pytmx.TiledTileLayer)]
        self.colliders: list[pygame.Rect] = []
        self.interact: list[Trigger] = []
        self.objects: list[TiledObject] = []
        self._positions: dict[str, Position] = {}

        self.setup()

    def get_position(self, name: str) -> Position:
        return self._positions.get(name)

    def setup(self):
        # Draw ground
        for layer in self.tiled_layers:
            for x, y, gid in layer:
                if not gid:
                    continue
                tile_image = self.data.get_tile_image_by_gid(gid)
                self.ground.blit(tile_image, (x * self.tile_width, y * self.tile_height))
        # Get objects
        for layer in self.objects_layers:
            for tiled_object in layer:
                tiled_object: pytmx.TiledObject
                if layer.name == "collision":
                    collider = pygame.Rect(tiled_object.x, tiled_object.y, tiled_object.width, tiled_object.height)
                    self.colliders.append(collider)
                    continue
                if layer.name == "interactions":
                    interact = Trigger(tiled_object.name, tiled_object.x, tiled_object.y, tiled_object.width,
                                       tiled_object.height)
                    self.interact.append(interact)
                    continue
                if layer.name == "positions":
                    position = Position(tiled_object.name, (tiled_object.x, tiled_object.y), tiled_object.properties)
                    self._positions[position.name] = position
                    continue
                if layer.name == "nodes":
                    ...
                image = tiled_object.image
                if not image:
                    continue
                position = tiled_object.x, tiled_object.y
                properties = tiled_object.properties
                # TODO: Add collider list for TiledObject
                collider_objects = tiled_object.properties["colliders"] if "colliders" in properties else []
                collider_list = []
                for collider_object in collider_objects:
                    if collider_object.name == "trigger":
                        continue
                    collider = pygame.Rect(collider_object.x, collider_object.y, collider_object.width, collider_object.height)
                    collider_list.append(collider)
                sorted_by_center = "center" if "centered" in properties else "bottom"
                self.objects.append(TiledObject(position, image, collider_list, sorted_by_center))
        # Get player start position or player enter instead
        # self.player_position = self.positions["player_start"] if self.start else self.positions["player_enter"]
