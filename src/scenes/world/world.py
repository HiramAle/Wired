from __future__ import annotations
import pygame
import engine.time as game_time
import engine.input as game_input
import engine.assets as game_assets
import engine.scene.scene_manager as scene_manager
from engine.scene.scene_manager import Scene
from src.constants.colors import BLACK_SPRITE
from src.scenes.world.npc import NPC
from src.scenes.world.sprite import Sprite
from src.scenes.world.zone import Zone
from src.constants.colors import DARK_BLACK_MOTION
from src.scenes.pause_menu.pause import Pause


class World(Scene):
    def __init__(self):
        super().__init__("world")
        # Day and time
        self.day_time = 360
        self.day_speed = 1.4
        self.week_day = 0
        # Daytime transition
        self.sky_surface = pygame.Surface(self.display.get_size())
        self.day_color = [255, 255, 255]
        self.night_color = (38, 101, 189)
        # Actors
        self.npc_list = [NPC("kat", (0, 0))]
        self.zone = Zone("playershouse", self.npc_list)
        self.overlay = game_assets.images_world["overlay"]
        self.hour = Sprite((78 + 16, 32), pygame.Surface((1, 1)))
        self.zone.npc_list[0].position = self.zone.map.get_position("kat").tuple
        self.next_zone = None
        self.player = self.zone.player
        # Zone transition
        self.transitionSpeed = 500
        self.alpha = 0
        self.fade_in = True
        self.fade_out = False
        self.fade_surface = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)

    def time_string(self):
        hours = int(self.day_time / 60)
        minutes = (int(self.day_time % 60) // 10) * 10
        time_string = "{:02d}:{:02d}".format(hours, minutes)
        return time_string

    def update_zone_transition(self):
        if not self.next_zone:
            return
        if self.fade_in:
            self.alpha += self.transitionSpeed * game_time.dt
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
                self.fade_out = True
        if self.fade_out:
            self.next_zone.update()
            self.alpha -= self.transitionSpeed * game_time.dt
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_out = False
                self.fade_in = True
                self.zone = self.next_zone
                self.next_zone = None

    def change_zone(self, zone: str):
        self.next_zone = Zone(zone, self.npc_list, self.zone.name)

    def update(self):
        # Day and time
        self.day_time += self.day_speed * game_time.dt
        if self.day_time >= 1320:
            self.day_time = 360
            self.week_day += 1
            if self.week_day > 6:
                self.week_day = 0
        # Daytime transition
        if self.day_time >= 1200:
            for index, value in enumerate(self.night_color):
                if self.day_color[index] > value:
                    self.day_color[index] -= 2 * game_time.dt
        for npc in self.npc_list:
            npc.pathing(self.day_time)
        self.update_zone_transition()
        self.zone.update()

        if game_input.keyboard.keys["esc"]:
            scene_manager.change_scene(self, Pause(0))

    def render(self) -> None:
        # Render zone
        self.zone.render()
        self.display.blit(self.zone.display, (0, 0))
        # Daytime transition
        self.sky_surface.fill(self.day_color)
        self.display.blit(self.sky_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.display.blit(self.overlay, (16, 16))
        self.hour.image = game_assets.fonts["monogram"].render(self.time_string(), 16, BLACK_SPRITE)
        self.hour.render(self.display)

        if self.next_zone:
            if self.fade_in:
                self.display.blit(self.zone.display, (0, 0))
            if self.fade_out:
                self.next_zone.render()
                self.display.blit(self.next_zone.display, (0, 0))
            self.fade_surface.fill(DARK_BLACK_MOTION)
            self.fade_surface.set_alpha(self.alpha)
            self.display.blit(self.fade_surface, (0, 0))
