from __future__ import annotations

import pygame

import src.scene.core.scene_manager as scene_manager
import src.engine.input as game_input
import src.engine.time as game_time
import src.engine.data as data
import src.scene.loading.loading as loading
import src.engine.assets as assets
from src.scene.core.scene import Scene
from src.entities.player import Player
from src.game_object.sprite import SpriteGroup, Sprite
from src.constants.colors import *
from src.gui.image import GUIImage
from src.entities.camera import Camera
from src.map.tiled_map import TiledMap
from src.scene.cables.order import OrderCable
from src.scene.subnetting.subnetting import Subnetting
from src.dialog.dialog_system import DialogManager
from src.entities.npc import NPC
from src.engine.world import instance as world
from src.constants.locals import *


class CustomGroup(SpriteGroup):
    def __init__(self):
        super().__init__()

    def sprites(self):
        return sorted(self._sprites, key=lambda sprite_: sprite_.y)


class Sky:
    def __init__(self):
        self.sky_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def render(self, display: pygame.Surface):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * game_time.dt

        self.sky_surface.fill(self.start_color)
        display.blit(self.sky_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class TestMap(Scene):
    def __init__(self, name: str):
        super().__init__(name)
        self.group = SpriteGroup()
        self.collisions = SpriteGroup()
        self.tiled_objects = CustomGroup()
        self.triggers = SpriteGroup()
        self.map = TiledMap(data.maps[name])
        self.player = Player(self, self.map.player_position, self.collisions, self.triggers, self.tiled_objects)
        self.camera = Camera(*self.map.background.get_size())
        self.camera._entity = self.player
        self.camera.position = self.player.x - 320, self.player.y - 180
        self.night_surface = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.night_alpha = 0
        GUIImage("map", (0, 0), self.map.background, self.group, layer=1, centered=False)
        self.tiled_objects.add(*self.map.objects)
        self.collisions.add(*self.map.collisions)
        self.triggers.add(*self.map.interactions)
        self.dialog = DialogManager(self.display)
        self.npcs = SpriteGroup()
        for npc in self.map.npcs:
            NPC(self, npc.name, npc.position, self.collisions, self.player, self.tiled_objects, self.npcs)
        self.lamps = SpriteGroup()
        self.sky = Sky()

        # self.update()
        # self.render()

    def update(self) -> None:
        # self.player.update()
        self.tiled_objects.update()
        self.camera.update()
        self.dialog.update()

        for npc in self.npcs.sprites():
            npc: NPC
            if npc.talkable and game_input.keyboard.keys["interact"]:
                self.dialog.show_dialog(*npc.dialogs)

    def change_scene(self, name: str):
        if "playable" in name:
            scene_name = name.split("_")[2]
            if scene_manager.stack_scene[-2].name == scene_name:
                scene_manager.exit_scene()
            else:
                scene_manager.change_scene(self,
                                           loading.Loading(data.load_map, TestMap, (scene_name,), (scene_name,)),
                                           transition=True)
        else:
            scene_name = name.split("_")[1]
            scene_manager.change_scene(self, scenes[scene_name](), transition=True)

    def render(self) -> None:
        self.display.fill(DARK_BLACK_MOTION)
        self.group.render(self.display, self.camera.position)
        self.tiled_objects.render(self.display, self.camera.position)
        if game_input.keyboard.keys["backspace"]:
            world.day_time = 1140
        if world.day_time >= 1140:
            self.sky.render(self.display)
        self.dialog.render()
        time_surface = assets.fonts["monogram"].render(world.time_string(), 32)
        self.display.blit(time_surface, (570, 10))


scenes = {"cables": OrderCable, "subnetting": Subnetting, "playable": TestMap}
