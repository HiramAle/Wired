import pygame.draw

import src.engine.assets as assets
import src.engine.data as data
from src.scene.core.scene import Scene
from src.entities.player import Player
from src.game_object.sprite import SpriteGroup
from src.constants.colors import *
from src.gui.image import GUIImage
from src.entities.camera import Camera
from src.map.tiled_map import TiledMap


class CustomGroup(SpriteGroup):
    def __init__(self):
        super().__init__()

    @property
    def sprites(self):
        return sorted(self._sprites, key=lambda sprite: sprite.y)


class TestMap(Scene):
    def __init__(self):
        super().__init__("test_map")
        self.group = SpriteGroup()
        self.collisions = SpriteGroup()
        self.tiled_objects = CustomGroup()
        self.toppers = CustomGroup()
        # GUIImage("background", (0, 0), assets.images_misc["space_background"], self.group, centered=False)
        self.player = Player((169 * 2, 250 * 2), self.collisions, self.tiled_objects)
        self.camera = Camera()
        self.camera._entity = self.player
        self.map = TiledMap(data.tiled_map)
        self.tiled_objects.add(*self.map.objects)
        # map_image = self.map.make_map()
        # map_image.set_colorkey((0, 0, 0))
        GUIImage("map", (0, 0), self.map.background, self.group, layer=1, centered=False)
        # self.group.add(*self.map.obstacles)
        # self.collisions.add(*self.map.obstacles)
        # self.furniture.add(*self.map.furniture)
        # self.furniture.add(*self.map.toppers)

    def update(self) -> None:
        self.player.update()
        self.camera.update()

    def render(self) -> None:
        self.display.fill(BLACK_MOTION)
        self.group.render(self.display, self.camera.position)
        self.tiled_objects.render(self.display, self.camera.position)
        # self.furniture.render(self.display, self.camera.position)
        # self.toppers.render(self.display, self.camera.position)

        # for obstacle in self.map.obstacles:
        #     pygame.draw.rect(self.display, "cyan", obstacle.rect, 2)
