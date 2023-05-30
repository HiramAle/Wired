import pytmx
import pygame
from src.scenes.world.trigger import Trigger
from src.scenes.world.tiled_object import TiledObject
from src.scenes.world.position import Position
from engine.data import Data


class GameMap:
    def __init__(self, name: str):
        self.data = Data.maps.get(name)
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
        self.triggers: list[Trigger] = []
        self.objects: list[TiledObject] = []
        self._positions: dict[str, Position] = {}
        self.setup()

    @property
    def instant(self) -> pygame.Surface:
        surface = self.ground.copy()
        for tiled_object in self.objects:
            tiled_object.render(surface)
        return surface

    def get_position(self, name: str) -> Position:
        return self._positions.get(name)

    def setup(self):
        # Draw ground
        for layer in self.tiled_layers:
            for x, y, gid in layer:
                if not gid:
                    continue
                tile_image = self.data.get_tile_image_by_gid(gid)
                if not tile_image:
                    continue
                self.ground.blit(tile_image, (x * self.tile_width, y * self.tile_height))
        # Get objects
        for layer in self.objects_layers:
            for tiled_object in layer:
                tiled_object: pytmx.TiledObject
                if tiled_object.id == 691:
                    print(tiled_object.__dict__)
                    print(tiled_object.image)
                if layer.name == "collision":
                    collider = pygame.Rect(tiled_object.x, tiled_object.y, tiled_object.width, tiled_object.height)
                    self.colliders.append(collider)
                    continue
                if layer.name == "triggers":
                    self.triggers.append(Trigger(tiled_object))
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
                collider_objects = tiled_object.properties["colliders"] if "colliders" in properties else []
                collider_list = []
                for collider_object in collider_objects:
                    if collider_object.name == "trigger":
                        continue
                    collider = pygame.Rect(collider_object.x, collider_object.y, collider_object.width,
                                           collider_object.height)
                    collider_list.append(collider)
                sorted_by_center = "center" if "centered" in properties else "bottom"
                self.objects.append(TiledObject(position, image, collider_list, sorted_by_center))
        # Get player start position or player enter instead
        # self.player_position = self.positions["player_start"] if self.start else self.positions["player_enter"]
