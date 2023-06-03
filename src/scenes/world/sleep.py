import pygame
from engine.scene.scene import Scene
from src.scenes.world.game_map import GameMap
from src.scenes.world.player import Player
from engine.assets import Assets
from engine.input import Input
from engine.constants import Colors
from engine.ui.text import Text
from engine.objects.sprite import Sprite
from src.scenes.world.time_manager import TimeManager
from engine.save_manager import instance as save_manager
from engine.playerdata import PlayerData
from threading import Thread, Event


class Sleep(Scene):
    def __init__(self):
        super().__init__("sleep")
        from engine.scene.scene_manager import SceneManager
        from src.scenes.world.world import World
        self.offset = pygame.Vector2(255 - 320, 215 - 180)
        self.player = Player((320, 180), [], [], [])
        self.player.direction = "down"
        self.player.action = "sleep"
        self.player.shadow = None
        self.map_image = GameMap("players_house").instant
        self.frame = Sprite((5, 52), Assets.images_world["sleep_overlay"], centered=False)
        self.title = Text((26, 76), "¡Día completado!", 32, Colors.SPRITE, shadow=True, shadow_opacity=50,
                          shado_color=Colors.SPRITE, centered=False)
        money_earned = PlayerData.inventory.money - save_manager.active_save.money
        self.money = Text((32, 122), f"Dinero obtenido       {money_earned}G", 16, Colors.SPRITE, shadow=True,
                          shadow_opacity=50, shado_color=Colors.SPRITE, centered=False)
        self.objets = Text((65, 184), "Objetos conseguidos", 16, Colors.SPRITE, shadow=True,
                           shadow_opacity=50, shado_color=Colors.SPRITE, centered=False)
        self.continue_text = Text((29, 276), "Presiona espacio para despertar", 16, Colors.SPRITE, opacity=125,
                                  centered=False)
        self.saved = Event()
        self.save_thread = Thread(target=self.update_day())
        self.save_thread.start()
        self.scene_manager = SceneManager
        self.world = World
        self.changed = Event()

    def update_day(self):
        TimeManager.restart()
        save_manager.active_save.week_day = TimeManager.current_day_of_week
        save_manager.save()
        self.saved.set()

    def change_zone(self):
        self.scene_manager.change_scene(self.world(), True, True)

    def update(self) -> None:
        self.player.animate()
        if self.saved.is_set():
            if Input.keyboard.keys["space"] and not self.scene_manager.transitioning:
                self.change_zone()

    def render(self) -> None:
        self.display.fill(Colors.SPRITE)
        self.display.blit(self.map_image, -self.offset)
        self.player.render(self.display)

        self.frame.render(self.display)
        self.title.render(self.display)
        self.money.render(self.display)
        self.objets.render(self.display)
        if self.saved.is_set():
            self.continue_text.render(self.display)
