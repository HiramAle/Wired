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
from engine.constants import Colors
from src.scenes.world.player import Player
from src.scenes.dialog_scene.dialog_scene import DialogScene
from src.scenes.tutorial.tutorial import Tutorial
from engine.objects.sprite import Sprite, SpriteGroup
from engine.ui.text import Text
from engine.save_manager import instance as save_manager


class Notification(Sprite):
    def __init__(self, position: tuple, text: str, seconds: int, *groups):
        super().__init__(position, Assets.images_misc["notification"], *groups)
        self.pivot = self.Pivot.TOP_LEFT
        self.text = Text((self.x + 11, self.y + 15), text, 16, Colors.SPRITE, centered=False, shadow=True,
                         shadow_opacity=50)
        self.timer = Timer(seconds)
        self.timer.start()

    def update(self, *args, **kwargs):
        if self.timer.update():
            self.kill()

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.text.render(display)


class Zone(Scene):
    def __init__(self, name: str, npc_list: list[NPC], player: Player, change_zone: callable, before=""):
        super().__init__(name)
        self.zone_before = before
        self.map = GameMap(name)
        self.location_type = "outside" if name in ["village", "city"] else "inside"
        self.npc_list = npc_list
        self.debug = False
        self.map_colliders = self.map.colliders
        self.map_objects = self.map.objects
        self.map_triggers = self.map.triggers
        self.player = player
        # self.player.position = self.map.get_position(f"player_{before}").tuple
        # self.player.direction = self.map.get_position(f"player_{before}").properties["direction"]
        self.player.collisions = []
        self.player.collisions = self.map_colliders + [npc.collider for npc in self.npcs]
        self.camera = Camera(self.map.width, self.map.height)
        self.camera.actor_tracking = self.player
        self.camera.position = self.player.x - 320, self.player.y - 180
        self.notification = SpriteGroup()
        self.obj: TiledObject | None = None
        for obj in self.map_objects:
            self.player.collisions.extend(obj.colliders)
        for npc in self.npcs:
            npc.position = self.map.get_position(npc.name).position
            npc.direction = self.map.get_position(npc.name).properties["direction"]
        self.change_zone = change_zone
        self.zone_objets = []
        self.zone_objets.append(self.player)
        self.zone_objets.extend(self.map_objects)
        self.zone_objets.extend(self.npcs)

    def start_zone(self):
        print(f"player_{self.zone_before}")
        self.player.position = self.map.get_position(f"player_{self.zone_before}").tuple
        self.player.direction = self.map.get_position(f"player_{self.zone_before}").properties["direction"]
        self.camera.position = self.player.x - 320, self.player.y - 180
        if self.name == "players_house" and not save_manager.active_save.tasks.get("meet_kat", None):
            Notification((30, 280), "Nueva mision añadida\nRevisa tu inventario\npara verla", 5,
                         self.notification)
            save_manager.active_save.tasks["meet_kat"] = False
            save_manager.active_save.tasks["mysteries_of_celestia"] = False

    @property
    def npcs(self) -> list[NPC]:
        return [npc for npc in self.npc_list if npc.current_zone == self.name]

    def update_triggers(self):
        for trigger in self.map_triggers:
            if not trigger.colliderect(self.player.collider):
                continue
            if not trigger.interact():
                continue
            from engine.scene.scene_manager import SceneManager
            if trigger.type == "zone":
                self.change_zone(trigger.zone)
            if trigger.type == "scene":
                if trigger.name == "cables":
                    from engine.inventory import Inventory
                    if not Inventory.has_enough("connector", 2) or not Inventory.has_enough("cable", 1):
                        Notification((30, 280), "Necesitas mas cable y\nconectorespara crear un\ncable de Red", 3,
                                     self.notification)
                        return
                if trigger.name == "subnetting" and self.name == "reception":
                    SceneManager.change_scene(SceneManager.scenes_by_name[trigger.scene]("Hotel", 1))
                else:
                    SceneManager.change_scene(SceneManager.scenes_by_name[trigger.scene]())
                if trigger.name != "store" and not save_manager.active_save.tutorials[trigger.scene]:
                    SceneManager.change_scene(Tutorial(trigger.scene), True)

            if trigger.type == "save":
                SceneManager.change_scene(SceneManager.scenes_by_name["sleep"](), True, True)

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

    @property
    def closest_npc(self) -> NPC | None:
        if not self.npcs:
            return None
        return min(self.npcs, key=lambda npc: npc.player_distance)

    def update_npcs(self):
        if not self.npcs:
            return
        for npc in self.npcs:
            npc.update()

        if self.closest_npc.interact():
            dialog_index = 0
            if self.closest_npc.name == "Roy":
                roy_known = save_manager.active_save.status.get("roy_known", None)
                if roy_known:
                    dialog_index = 1
                else:
                    save_manager.active_save.status["roy_known"] = True
                if "meet_roy" in save_manager.active_save.tasks.keys():
                    if not save_manager.active_save.tasks["meet_roy"]:
                        save_manager.active_save.tasks["meet_roy"] = True
                        save_manager.active_save.tasks["subnetting_reception"] = False
                        Notification((30, 280), "Nueva mision añadida\nRevisa tu inventario\npara verla", 3,
                                     self.notification)
            elif self.closest_npc.name == "Kat":
                if "meet_kat" in save_manager.active_save.tasks.keys():
                    if not save_manager.active_save.tasks["meet_kat"]:
                        save_manager.active_save.tasks["meet_kat"] = True
                        save_manager.active_save.tasks["meet_chencho"] = False
                        Notification((30, 280), "Nueva mision añadida\nRevisa tu inventario\npara verla", 3,
                                     self.notification)
            elif self.closest_npc.name == "Chencho":
                if "meet_chencho" in save_manager.active_save.tasks.keys():
                    if not save_manager.active_save.tasks["meet_chencho"]:
                        save_manager.active_save.tasks["meet_chencho"] = True
                        save_manager.active_save.tasks["meet_roy"] = False
                        Notification((30, 280), "Nueva mision añadida\nRevisa tu inventario\npara verla", 3,
                                     self.notification)
            elif self.closest_npc.name == "Ale":
                if "subnetting_reception" in save_manager.active_save.tasks.keys():
                    if not save_manager.active_save.tasks["subnetting_reception"]:
                        save_manager.active_save.tasks["subnetting_reception"] = True
                        # save_manager.active_save.tasks["meet_roy"] = False
                        # Notification((30, 280), "Nueva mision añadida\nRevisa tu inventario\npara verla", 3,
                        #              self.notification)

            from engine.scene.scene_manager import SceneManager
            SceneManager.change_scene(DialogScene(self.closest_npc, self, dialog_index))
            self.update_interact_tasks(self.closest_npc.name)

    def update_interact_tasks(self, actor: str):
        from src.scenes.world.tasks import TaskManager
        from engine.save_manager import instance as save_manager

        tasks = TaskManager.get_tasks_from_type("talk")
        print(f"interaction tasks {tasks}")
        for task_id in tasks:
            task = TaskManager.get_task(task_id)
            if actor.lower() == task.objective:
                TaskManager.complete_task(task_id)
            # for objective in save_manager.active_save.objectives.keys():
            #     if self.closest_npc.name.lower() in objective:
            #         if TaskManager.check_task_completion(0):
            #             TaskManager.complete_task(0)

    def update_player_emote(self):
        if any([trigger.colliderect(self.player.collider) for trigger in self.map_triggers]):
            self.player.set_emote("alert")
        elif self.closest_npc.player_distance <= 50:
            self.player.set_emote("ask")
        elif self.player.emote:
            self.player.emote.animation.rewind()
            self.player.emote = None

    def update(self) -> None:
        self.player.update()
        self.camera.update()
        self.update_player_emote()
        self.update_triggers()
        self.notification.update()
        self.update_npcs()

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.display.blit(self.map.ground, -self.camera.offset)
        for zone_object in sorted(self.zone_objets, key=lambda sprite: sprite.sort_point):
            zone_object.render(self.display, self.camera.offset)

        if self.obj:
            self.obj.render(self.display)

        self.notification.render(self.display)
