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
from src.scenes.pause_menu.pause import Pause
from engine.audio import AudioManager
from src.scenes.world.player import Player
from src.scenes.world.time_manager import TimeManager
from src.scenes.world.zone_manager import ZoneManager
# from src.scenes.world.tasks import TaskManager, Task
from engine.save_manager import instance as save_manager
from engine.ui.text import Text
# from engine.inventory import Inventory
from src.scenes.dialog_scene.portrait import PlayerPortrait
from engine.playerdata import PlayerData


class NightEffect(Sprite):
    def __init__(self):
        super().__init__((0, 0), pygame.Surface((640, 360)))
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
        self.night = NightEffect()
        # ----------
        self.player = Player((0, 0), [], [], [])
        # self.npc_list = [NPC("Kat", (0, 0), self.player), NPC("Arian", (0, 0), self.player),
        #                  NPC("Chencho", (0, 0), self.player), NPC("Altair", (0, 0), self.player),
        #                  NPC("Kike", (0, 0), self.player), NPC("Jordi", (0, 0), self.player),
        #                  NPC("Letty", (0, 0), self.player), NPC("Ale", (0, 0), self.player),
        #                  NPC("Roy", (0, 0), self.player), NPC("Liz", (0, 0), self.player),
        #                  NPC("Angel", (0, 0), self.player), NPC("Zazu", (0, 0), self.player),
        #                  NPC("Juliette", (0, 0), self.player), NPC("Cecy", (0, 0), self.player),
        #                  NPC("Juan", (0, 0), self.player)]
        self.npc_list = [NPC("Kat", (0, 0), self.player), NPC("Roy", (0, 0), self.player),
                         NPC("Chencho", (0, 0), self.player)]
        self.zone = Zone("players_house", self.npc_list, self.player, self.new_zone)
        # ----------
        self.overlay = Assets.images_world["overlay"]
        self.hour = Text((93, 32), TimeManager.formatted_time(), 16, Colors.SPRITE, shadow=True, shadow_opacity=50)
        self.money = Text((93, 50), str(PlayerData.inventory.money), 16, Colors.SPRITE, shadow=True, shadow_opacity=50)
        self.portrait = PlayerPortrait()
        self.next_zone: Zone | None = None

        # Zone transition
        self.transitionSpeed = 500
        self.alpha = 0
        self.fade_in = True
        self.fade_out = False
        self.fade_surface = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.zone.player.can_move = True
        self.zone.start_zone()
        self.transitioning = False

    def check_for_end_day(self):
        if not TimeManager.day_ended or self.transitioning:
            return
        from engine.scene.scene_manager import SceneManager
        from src.scenes.world.sleep import Sleep
        SceneManager.change_scene(Sleep(), True, True)
        self.transitioning = True

    def update_zone_transition(self):
        if not self.next_zone:
            return
        if self.fade_in:
            self.alpha += self.transitionSpeed * Time.dt
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
                self.fade_out = True
                self.zone = self.next_zone
                self.zone.start_zone()
        if self.fade_out:
            self.next_zone.update()
            self.alpha -= self.transitionSpeed * Time.dt
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_out = False
                self.fade_in = True
                self.next_zone = None
                self.zone.player.can_move = True

    def render_zone_transition(self):
        if not self.next_zone:
            return
        if self.fade_in:
            self.display.blit(self.zone.display, (0, 0))
        if self.fade_out:
            self.next_zone.render()
            self.display.blit(self.next_zone.display, (0, 0))
        self.fade_surface.fill(Colors.DARK)
        self.fade_surface.set_alpha(self.alpha)
        self.display.blit(self.fade_surface, (0, 0))

    def new_zone(self, zone: str, before=""):
        self.zone.player.can_move = False
        self.zone.player.action = "idle"
        zone_before = self.zone.name if before == "" else before
        self.next_zone = Zone(zone, self.npc_list, self.player, self.new_zone, zone_before)

    def update(self):
        self.update_zone_transition()
        self.zone.update()
        TimeManager.update()
        self.night.update()
        self.portrait.update()

        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            SceneManager.change_scene(Pause(self.new_zone))

        self.check_for_end_day()

        if Input.keyboard.keys["backspace"]:
            self.portrait.status = "talk"

    def render(self) -> None:
        # Render zone
        self.zone.render()
        self.display.blit(self.zone.display, (0, 0))
        self.display.blit(self.overlay, (16, 16))
        self.hour.text = TimeManager.formatted_time()
        self.money.text = str(PlayerData.inventory.money)
        self.hour.render(self.display)
        self.money.render(self.display)
        self.portrait.render(self.display)
        self.render_zone_transition()
        if self.zone.location_type == "outside":
            self.night.render(self.display)
