import pygame
from engine.window import Window
from engine.input import Input
from engine.scene.scene import Scene
# from src.entities.camera import Camera
from engine.time import Timer
from engine.assets import Assets
from src.scenes.world.camera import Camera
from src.scenes.world.npc import NPC
from src.scenes.world.game_map import GameMap
from src.scenes.world.tiled_object import TiledObject
from src.constants.colors import BLACK_SPRITE
from src.scenes.world.player import Player
from src.scenes.dialog_scene.dialog_scene import DialogScene
from src.scenes.tutorial.tutorial import Tutorial
from engine.objects.sprite import Sprite, SpriteGroup
from engine.ui.text import Text


class Notification(Sprite):
    def __init__(self, position: tuple, text: str, *groups):
        super().__init__(position, Assets.images_misc["notification"], *groups)
        self.pivot = self.Pivot.TOP_LEFT
        self.text = Text((self.x + 11, self.y + 15), text, 16, BLACK_SPRITE, centered=False)
        self.timer = Timer(3)
        self.timer.start()

    def update(self, *args, **kwargs):
        if self.timer.update():
            self.kill()

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.text.render(display)


class Zone(Scene):
    def __init__(self, name: str, npc_list: list[NPC], player: Player, before=""):
        super().__init__(name)
        self.map = GameMap(name)
        self.npc_list = npc_list
        self.debug = False
        self.map_colliders = self.map.colliders
        self.map_objects = self.map.objects
        self.map_triggers = self.map.triggers
        self.player = player
        self.player.position = self.map.get_position(f"player_{before}").tuple
        self.player.direction = self.map.get_position(f"player_{before}").properties["direction"]
        self.player.collisions = []
        self.player.collisions = self.map_colliders
        self.camera = Camera(self.map.width, self.map.height)
        self.camera.actor_tracking = self.player
        self.camera.position = self.player.x - 320, self.player.y - 180
        self.notification = SpriteGroup()
        self.obj: TiledObject | None = None
        for obj in self.map_objects:
            self.player.collisions.extend(obj.colliders)
        for npc in self.npcs:
            print(npc.name)
            npc.position = self.map.get_position(npc.name).position
            npc.direction = self.map.get_position(npc.name).properties["direction"]

    @property
    def npcs(self) -> list[NPC]:
        return [npc for npc in self.npc_list if npc.current_zone == self.name]

    def update_triggers(self):
        from engine.save_manager import instance as save_manager
        for trigger in self.map_triggers:
            if trigger.colliderect(self.player.collider) and trigger.interact():
                from engine.scene.scene_manager import SceneManager
                if trigger.type == "zone":
                    SceneManager.get_active_scene().change_zone(trigger.zone)
                if trigger.type == "scene":
                    if trigger.name == "cables":
                        from engine.inventory import Inventory
                        if not Inventory.has_enough("connector", 2) or not Inventory.has_enough("cable", 1):
                            Notification((30, 280), "Necesitas mas cable y\nconectorespara crear un\ncable de Red",
                                         self.notification)
                            return
                    SceneManager.change_scene(SceneManager.scenes_by_name[trigger.scene]())
                    if trigger.name != "store" and not save_manager.active_save.tutorials[trigger.scene]:
                        SceneManager.change_scene(Tutorial(trigger.scene), True)

                if trigger.type == "save":
                    save_manager.active_save.save()

    def move_objects(self):
        if any([obj.hovered(self.camera.offset) for obj in self.map.objects]):
            Window.set_cursor("hand")
        elif not self.obj:
            Window.set_cursor("arrow")
        if self.obj:
            Window.set_cursor("grab")

        if self.obj:
            self.obj.x = Input.mouse.x - self.obj.rect.width / 2
            self.obj.y = Input.mouse.y - self.obj.rect.height / 2
            if Input.mouse.buttons["left"]:
                x = Input.mouse.x + self.camera.x - self.obj.rect.width / 2
                y = Input.mouse.y + self.camera.y - self.obj.rect.height / 2
                self.obj.x, self.obj.y = x, y
                self.map.objects.append(self.obj)
                self.obj = None
        else:
            for obj in self.map.objects:
                if obj.clicked(self.camera.offset):
                    self.obj = obj
                    self.map.objects.remove(self.obj)
                    break

    def update(self) -> None:
        self.player.update()
        self.camera.update()

        self.update_triggers()
        self.notification.update()

        for npc in self.npcs:
            npc.update()
            if npc.interact():
                from engine.scene.scene_manager import SceneManager
                SceneManager.change_scene(DialogScene(npc))
            # print(f"{npc.name} is at {npc.player_distance}px from player")

    def render(self) -> None:
        self.display.fill(BLACK_SPRITE)
        self.display.blit(self.map.ground, -self.camera.offset)
        for obj in sorted(
                [self.player] + self.map_objects + [npc for npc in self.npc_list if npc.current_zone == self.name],
                key=lambda sprite: sprite.sort_point):
            obj.render(self.display, self.camera.offset)

        if self.obj:
            self.obj.render(self.display)

        self.notification.render(self.display)
