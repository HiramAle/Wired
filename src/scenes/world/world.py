from __future__ import annotations
import pygame
from engine.time import Time
from engine.input import Input
from engine.assets import Assets
from engine.scene.scene_manager import Scene
from src.constants.colors import BLACK_SPRITE
from src.scenes.world.npc import NPC
from src.scenes.world.sprite import Sprite
from src.scenes.world.zone import Zone
from engine.constants import Colors
from src.scenes.test_scene import TestScene
from engine.audio import AudioManager
from src.scenes.world.player import Player
from src.scenes.world.time_manager import TimeManager
from src.scenes.world.zone_manager import ZoneManager


class NightEffect(Sprite):
    def __init__(self):
        super().__init__((0, 0), pygame.Surface((640, 320)))
        self.day_color = [255, 255, 255]
        self.night_color = (38, 101, 189)

    def update(self):
        if TimeManager.current_time_minutes < 1200:
            return
        for index, value in enumerate(self.night_color):
            if self.day_color[index] > value:
                self.day_color[index] -= 2 * Time.dt

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)) -> None:
        self.image.fill(self.day_color)
        display.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class World(Scene):
    def __init__(self):
        super().__init__("world")
        AudioManager.play_music("exploration")
        # pygame.mixer.music.set_volume(1)
        self.night = NightEffect()
        # ----------
        self.player = Player((0, 0), [], [], [])
        self.npc_list = [NPC("Kat", (0, 0), self.player), NPC("Arian", (0, 0), self.player),
                         NPC("Chencho", (0, 0), self.player), NPC("Altair", (0, 0), self.player),
                         NPC("Kike", (0, 0), self.player), NPC("Jordi", (0, 0), self.player)]
        self.zone = Zone("players_house", self.npc_list, self.player)
        # ----------
        self.overlay = Assets.images_world["overlay"]
        self.hour = Sprite((78 + 16, 32), pygame.Surface((1, 1)))
        # self.zone.npc_list[0].position = self.zone.map.get_position("kat").tuple
        self.next_zone = None

        # Zone transition
        self.transitionSpeed = 500
        self.alpha = 0
        self.fade_in = True
        self.fade_out = False
        self.fade_surface = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)

    def update_zone_transition(self):
        if not self.next_zone:
            return
        if self.fade_in:
            self.alpha += self.transitionSpeed * Time.dt
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
                self.fade_out = True
        if self.fade_out:
            self.next_zone.update()
            self.alpha -= self.transitionSpeed * Time.dt
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_out = False
                self.fade_in = True
                self.zone = self.next_zone
                self.next_zone = None

    def change_zone(self, zone: str):
        self.next_zone = Zone(zone, self.npc_list, self.player, self.zone.name)

    def update(self):
        self.update_zone_transition()
        self.zone.update()

        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            SceneManager.change_scene(TestScene())

    def render(self) -> None:
        # Render zone
        self.zone.render()
        self.display.blit(self.zone.display, (0, 0))
        self.display.blit(self.overlay, (16, 16))
        self.hour.image = Assets.fonts["monogram"].render(TimeManager.formatted_time(), 16, BLACK_SPRITE)
        self.hour.render(self.display)

        if self.next_zone:
            if self.fade_in:
                self.display.blit(self.zone.display, (0, 0))
            if self.fade_out:
                self.next_zone.render()
                self.display.blit(self.next_zone.display, (0, 0))
            self.fade_surface.fill(Colors.DARK)
            self.fade_surface.set_alpha(self.alpha)
            self.display.blit(self.fade_surface, (0, 0))
