import pygame
from engine.input import Input
from engine.assets import Assets
from engine.save_manager import instance as save_manager
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
        super().__init__(position, save_manager.active_save.sprite_sheet, collisions)
        self.interactions = interactions
        self.objects = objects
        for obj in objects:
            self.collisions.extend(obj.colliders)
        self.can_move = True

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

    def set_emote(self, emote: str):
        if self.emote:
            return
        self.emote = Emote((self.x, self.y - 24), Assets.animations["emotes"][emote])
        self.emote.animation.play()

    def update(self):
        if self.can_move:
            self.input()
            self.move()
            self.update_status()
        self.animate()
        if self.emote:
            self.emote.update()
            self.emote.position = (self.rect.centerx, self.rect.top - 24)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display, offset)
        if self.emote:
            self.emote.render(display, offset)
