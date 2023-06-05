import enum

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
# from engine.save_manager import instance as save_manager
from engine.playerdata import PlayerData
from src.scenes.world.trigger import Trigger
from engine.dialog_manager import Dialog
from engine.data import Data
from engine.audio import AudioManager
from src.scenes.world.key_hint import KeyHint


class Zone(Scene):
    def __init__(self, name: str, npc_list: list[NPC], player: Player, change_zone: callable, notify: callable, world,
                 before=""):
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
        self.player.collisions = []
        self.player.collisions = self.map_colliders + [npc.collider for npc in self.npcs]
        self.camera = Camera(self.map.width, self.map.height)
        self.camera.actor_tracking = self.player
        self.camera.position = self.player.x - 320, self.player.y - 180
        self.notification = SpriteGroup()
        self.obj: TiledObject | None = None
        for obj in self.map_objects:
            self.player.collisions.extend(obj.colliders)

        self.change_zone = change_zone
        self.zone_objets = []
        self.zone_objets.append(self.player)
        self.zone_objets.extend(self.map_objects)
        self.zone_objets.extend(self.npcs)
        self.notify = notify
        self.world = world
        self.npc: NPC | None = None

        self.step_timer = Timer(0.3)
        self.step_timer.start()
        self.key_hint = KeyHint(KeyHint.Type.PAUSE)

    def start_zone(self):
        self.player.position = self.map.get_position(f"player_{self.zone_before}").tuple
        self.player.direction = self.map.get_position(f"player_{self.zone_before}").properties["direction"]
        self.camera.position = self.player.x - 320, self.player.y - 180
        # if self.name == "players_house" and not PlayerData.tasks.tasks:
        #     PlayerData.add_task("meet_kat")
        for npc in self.npcs:
            npc_position = self.map.get_position(npc.name)
            if not npc_position:
                continue
            npc.position = npc_position.position
            npc.direction = npc_position.properties.get("direction", "down")
            npc.action = npc_position.properties.get("action", "idle")

    @property
    def npcs(self) -> list[NPC]:
        return [npc for npc in self.npc_list if npc.current_zone == self.name]

    def get_trigger(self) -> Trigger | None:
        for trigger in self.map_triggers:
            if not trigger.colliderect(self.player.collider):
                continue
            return trigger
        return None

    def check_triggers(self):
        if not Input.keyboard.keys["interact"]:
            return
        trigger = self.get_trigger()
        if not trigger:
            return
        # Check Zone and Scene requirements
        match trigger.name:
            case "zone_village":
                if not PlayerData.tasks.is_completed("meet_kat"):
                    self.notify("Habla con Kat antes\nde salir", 3)
                    return
            case "zone_company":
                if not PlayerData.tasks.is_completed("meet_chencho"):
                    self.notify("Habla con Chencho antes\nde continuar", 3)
                    return
            case "cables":
                if not PlayerData.inventory.how_many("cable") >= 1 or not PlayerData.inventory.has_enough("connector",
                                                                                                          2):
                    self.notify("Necesitas mas cable y conectores para crear cable de Red", 3)
                    return
            case "subnetting":
                print(f"subnetting_{self.name}")
                print([task.id for task in PlayerData.tasks.current_tasks])
                if not PlayerData.tasks.has_incomplete(f"subnetting_{self.name}"):
                    self.notify("Aún no puedes trabajar aquí", 3)
                    return
                problem_data = Data.subnetting[self.name]
                if not PlayerData.inventory.has_enough("cable_straight", problem_data.subnetsNeeded):
                    self.notify(f"Necesitas {problem_data.subnetsNeeded} de cable directo.", 3)
                    return
            case "routing":
                if not PlayerData.tasks.has_incomplete(f"routing_{self.name}"):
                    self.notify("Aún no puedes trabajar aquí", 3)
                    return
                problem_data = Data.routing[self.name]
                if not PlayerData.inventory.has_enough("serial_cable", problem_data.cables):
                    self.notify(f"Necesitas {problem_data.cables} de cable serial.", 3)
                    return

        # Execute code depending on the trigger type
        from engine.scene.scene_manager import SceneManager
        match trigger.type:
            case "scene":
                if trigger.scene in ["subnetting", "routing"]:
                    SceneManager.change_scene(SceneManager.scenes_by_name[trigger.scene](self.name))
                else:
                    SceneManager.change_scene(SceneManager.scenes_by_name[trigger.scene]())
                # Add tutorial if its needed
                if trigger.scene not in ["store", "sleep"] and not PlayerData.tutorials[trigger.scene]:
                    SceneManager.change_scene(Tutorial(trigger.scene), True)
            case "zone":
                self.change_zone(trigger.zone)
            case "save":
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

    def __move_npc(self):
        if any([npc.hovered(self.camera.offset) for npc in self.npcs]):
            Window.set_cursor("hand")
        elif not self.npc:
            Window.set_cursor("arrow")
        if self.npc:
            Window.set_cursor("grab")

        if self.npc:
            self.npc.x = Input.mouse.x + self.camera.x
            self.npc.y = Input.mouse.y + self.camera.y
            if Input.mouse.buttons["left"]:
                self.npc = None
        else:
            for npc in self.npcs:
                if npc.clicked(self.camera.offset):
                    self.npc = npc
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
            from engine.scene.scene_manager import SceneManager
            self.player.action = "idle"
            self.closest_npc.set_direction()
            SceneManager.change_scene(DialogScene(self.closest_npc, self, self.world))
            self.key_hint.deactivate()

    def update_player_emote(self):
        trigger = self.get_trigger()
        if not trigger:
            if self.player.emote:
                self.player.emote.animation.rewind()
                self.player.emote = None
        if trigger:
            self.player.set_emote("alert")
        if self.npcs:
            if self.closest_npc.player_distance <= 50:
                self.player.set_emote("ask")
            elif self.player.emote:
                self.player.emote.animation.rewind()
                self.player.emote = None

    def update_trigger_emote(self):
        trigger = self.get_trigger()
        if not trigger:
            return False
        self.key_hint.activate()
        if trigger.type == "zone":
            self.key_hint.hint_type = KeyHint.Type.ENTER
        elif trigger.type == "save":
            self.key_hint.hint_type = KeyHint.Type.SLEEP
        else:
            self.key_hint.hint_type = KeyHint.Type.INTERACT
        return True

    def update_npc_emote(self):
        if not self.npcs:
            return False
        if self.closest_npc.player_distance > 50:
            return False
        self.key_hint.activate()
        self.key_hint.hint_type = KeyHint.Type.TALK
        return True

    def dialog_update(self):
        self.player.animate()
        self.camera.update()
        for npc in self.npcs:
            npc.update()

    def update(self) -> None:
        self.player.update()
        self.camera.update()
        if not any([self.update_trigger_emote(), self.update_npc_emote()]):
            self.key_hint.deactivate()
        self.notification.update()
        self.check_triggers()
        self.update_npcs()

        if self.player.movement.magnitude() > 0:
            if self.step_timer.update():
                AudioManager.play_random_from("step")
                self.step_timer.start()

        if Input.keyboard.keys["backspace"]:
            for npc in self.npc_list:
                print(npc.name, npc.current_zone)

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.display.blit(self.map.ground, -self.camera.offset)
        for zone_object in sorted(self.zone_objets, key=lambda sprite: sprite.sort_point):
            zone_object.render(self.display, self.camera.offset)

        if self.obj:
            self.obj.render(self.display)

        self.notification.render(self.display)

        self.key_hint.render(self.display)
