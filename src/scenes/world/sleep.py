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


class Sleep(Scene):
    def __init__(self):
        super().__init__("sleep")
        self.offset = pygame.Vector2(255 - 320, 215 - 180)
        self.player = Player((320, 180), [], [], [])
        self.player.direction = "down"
        self.player.action = "sleep"
        self.player.shadow = None
        self.map_image = GameMap("players_house").instant
        self.frame = Sprite((5, 52), Assets.images_world["sleep_overlay"], centered=False)
        self.title = Text((26, 76), "¡Día completado!", 32, Colors.SPRITE, shadow=True, shadow_opacity=50,
                          shado_color=Colors.SPRITE, centered=False)
        from engine.save_manager import instance as save_manager
        from engine.inventory import Inventory
        money_earned = Inventory.money - save_manager.active_save.money
        self.money = Text((32, 122), f"Dinero obtenido       {money_earned}G", 16, Colors.SPRITE, shadow=True,
                          shadow_opacity=50, shado_color=Colors.SPRITE, centered=False)
        self.objets = Text((65, 184), "Objetos conseguidos", 16, Colors.SPRITE, shadow=True,
                           shadow_opacity=50, shado_color=Colors.SPRITE, centered=False)
        self.continue_text = Text((29, 276), "Presiona espacio para despertar", 16, Colors.SPRITE, opacity=125,
                                  centered=False)

    def update(self) -> None:
        from engine.scene.scene_manager import SceneManager
        self.player.animate()
        if Input.keyboard.keys["space"] and not SceneManager.transitioning:
            pygame.image.save(self.display, "screen_shoot.png")

            from src.scenes.world.world import World
            SceneManager.change_scene(World(), True, True)
            from engine.save_manager import instance as save_manager
            save_manager.active_save.save()
            TimeManager.restart()

    def render(self) -> None:
        self.display.fill(Colors.SPRITE)
        self.display.blit(self.map_image, -self.offset)
        self.player.render(self.display)

        self.frame.render(self.display)
        self.title.render(self.display)
        self.money.render(self.display)
        self.objets.render(self.display)
        self.continue_text.render(self.display)
