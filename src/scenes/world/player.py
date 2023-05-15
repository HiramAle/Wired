import pygame
from engine.input import Input
from engine.assets import Assets
from src.utils.json_saver import instance as save_manager
from src.scenes.world.trigger import Trigger
from src.constants.paths import USER_DATA
from src.scenes.world.actor import Actor, Emote
from src.scenes.world.tiled_object import TiledObject


class Player(Actor):
    def __init__(self,
                 position: tuple,
                 collisions: list[pygame.Rect],
                 objects: list[TiledObject],
                 interactions: list[Trigger]):
        path = f"{USER_DATA}/saves/save_{save_manager.index}/sprite_sheet.png"
        super().__init__(position, path, collisions)
        self.interactions = interactions
        self.objects = objects
        self.active_trigger: None | Trigger = None
        for obj in objects:
            self.collisions.extend(obj.colliders)

    def __repr__(self):
        return f"Player {self.position}"

    def input(self):
        # Movement input
        self.movement.x, self.movement.y = 0, 0
        if Input.keyboard.keys["left"]:
            self.movement.x = - 1
        if Input.keyboard.keys["right"]:
            self.movement.x = 1
        if Input.keyboard.keys["up"]:
            self.movement.y = - 1
        if Input.keyboard.keys["down"]:
            self.movement.y = 1

        if Input.keyboard.keys["interact"]:
            if self.active_trigger:
                if "zone" in self.active_trigger.name:
                    to_zone = self.active_trigger.name.split("_")[1]
                    from engine.scene.scene_manager import SceneManager
                    world = SceneManager.get_active_scene()
                    world.change_zone(to_zone)
                elif "sleep" in self.active_trigger.name:
                    save_manager.game_save.save()

    def check_triggers(self):
        if self.active_trigger:
            if not self.collider.colliderect(self.active_trigger):
                self.active_trigger = None
                self.emote = None
                self.speed = 150
            return
        for trigger in self.interactions:
            if self.collider.colliderect(trigger):
                self.active_trigger = trigger
                if trigger.name == "stairs":
                    self.speed = 100
                    return
                self.emote = Emote((self.rect.centerx, self.rect.top + 24), Assets.animations["emotes"]["alert"])
                return

    def update(self):
        self.input()
        self.move()
        self.update_status()
        self.animate()
        self.check_triggers()
        if self.emote:
            self.emote.update()
            self.emote.position = (self.rect.centerx, self.rect.top - 24)
