import pygame
import src.engine.time as time
import src.engine.input as input
import src.engine.data as data
from src.entities.entity import Entity
from src.game_object.sprite import SpriteGroup
import src.utils.load as load
from src.constants.paths import *


class Player(Entity):
    def __init__(self, position: tuple, collision_group: SpriteGroup, *groups, **kwargs):
        super().__init__("player", position, *groups, **kwargs)
        self.speed = 150
        self.movement = pygame.Vector2(0, 0)
        self.collision_group = collision_group
        sprite_sheet = pygame.image.load(f"{USER_DATA}/saves/save_{data.active_save}/sprite_sheet.png").convert_alpha()
        self.animations = load.export_animation_frames(sprite_sheet)
        self.direction = "down"
        self.action = "idle"
        self.image = self.animations["idle"]["down"][0]
        self.frame_index = 0
        self.animation_speed = 10

    def animate(self):
        self.frame_index += time.dt * self.animation_speed

        if self.frame_index >= len(self.animations[self.action][self.direction]):
            self.frame_index = 0

        self.image = self.animations[self.action][self.direction][int(self.frame_index)]

    def set_movement(self):
        self.movement.x, self.movement.y = 0, 0
        if input.keyboard.keys["left"]:
            self.movement.x = - 1
            self.direction = "left"
        if input.keyboard.keys["right"]:
            self.movement.x = 1
            self.direction = "right"
        if input.keyboard.keys["up"]:
            self.movement.y = - 1
            self.direction = "up"
        if input.keyboard.keys["down"]:
            self.movement.y = 1
            self.direction = "down"
        if self.movement.magnitude() > 0:
            self.movement = self.movement.normalize()
            self.action = "walk"
        else:
            self.action = "idle"

    def collision(self, axis: str):
        for sprite in self.collision_group.sprites():
            if not self.rect.colliderect(sprite.rect):
                continue

            hit_box = self.rect
            if axis == "x":
                if self.movement.x > 0:
                    hit_box.right = sprite.rect.left
                if self.movement.x < 0:
                    hit_box.left = sprite.rect.right
                self.x = hit_box.centerx

            if axis == "y":
                if self.movement.y > 0:
                    hit_box.bottom = sprite.rect.top
                if self.movement.y < 0:
                    hit_box.top = sprite.rect.bottom
                self.y = hit_box.centery

    def update(self):
        self.set_movement()
        self.position_vector.x += self.movement.x * self.speed * time.dt
        self.collision("x")
        self.position_vector.y += self.movement.y * self.speed * time.dt
        self.collision("y")
        self.animate()
