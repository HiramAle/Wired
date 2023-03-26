import pygame
import src.engine.time as time
import src.engine.input as input
from src.entities.entity import Entity
from src.game_object.sprite import SpriteGroup


class Player(Entity):
    def __init__(self, position: tuple, collision_group: SpriteGroup, *groups, **kwargs):
        super().__init__("player", position, *groups, **kwargs)
        self.speed = 150
        self.movement = pygame.Vector2(0, 0)
        self.collision_group = collision_group



    def set_movement(self):
        self.movement.x, self.movement.y = 0, 0
        if input.keyboard.keys["left"]:
            self.movement.x = - 1
        if input.keyboard.keys["right"]:
            self.movement.x = 1
        if input.keyboard.keys["up"]:
            self.movement.y = - 1
        if input.keyboard.keys["down"]:
            self.movement.y = 1
        if self.movement.magnitude() > 0:
            self.movement = self.movement.normalize()

    def collision(self, axis: str):
        for sprite in self.collision_group.sprites:
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
