import pygame
from pytmx import TiledObject
from engine.input import Input


class Trigger(pygame.Rect):
    def __init__(self, tiled_object: TiledObject):
        super().__init__(tiled_object.x, tiled_object.y, tiled_object.width, tiled_object.height)
        self.name = tiled_object.name
        self.type = tiled_object.type
        self.interaction_type = tiled_object.properties["interaction_type"]
        self.zone = tiled_object.properties.get("zone", None)
        self.scene = tiled_object.properties.get("scene", None)
        self.direction = tiled_object.properties.get("direction", None)

    def interact(self) -> bool:
        if self.interaction_type == "collide":
            return True
        if Input.keyboard.keys["interact"]:
            return True
        return False

    def __repr__(self):
        return f"Trigger({self.name}, {self.type}, {self.interaction_type})"
