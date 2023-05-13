import random

import pygame
from src.entities.entity import Entity
from engine.objects.sprite import SpriteGroup
import src.utils.load as load
import engine.time as game_time
import engine.assets as assets


class Actor(Entity):
    def __init__(self, position: tuple, collisions: SpriteGroup, sprite_sheet_path: str, *groups, **kwargs):
        super().__init__(self.__class__.__name__.lower(), position, *groups, **kwargs)
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.animations = load.export_animation_frames(sprite_sheet)
        self.speed = 150
        self.movement = pygame.Vector2()
        self.collisions = collisions
        self.direction = "down"
        self.action = "idle"
        self.collider = pygame.Rect(0, 0, 28, 20)
        self.frame_index = 0
        self.animation_speed = random.randint(9, 11)
        self.shadow = assets.images_actors["actor_shadow"]

    def update_status(self):
        if self.movement.magnitude() > 0:
            self.action = "walk"
            if self.movement.x < 0:
                self.direction = "left"
            if self.movement.x > 0:
                self.direction = "right"
            if self.movement.x == 0:
                if self.movement.y < 0:
                    self.direction = "up"
                if self.movement.y > 0:
                    self.direction = "down"
        else:
            if self.action == "walk":
                self.action = "idle"

    def move(self):
        if self.movement.magnitude() > 1:
            self.movement = self.movement.normalize()
        self.x += self.movement.x * self.speed * game_time.dt
        self.collider.centerx = self.x
        self.collision("x")
        self.y += self.movement.y * self.speed * game_time.dt
        self.collider.bottom = self.rect.bottom
        self.collision("y")

    def animate(self):
        self.frame_index += game_time.dt * self.animation_speed
        if self.frame_index >= len(self.animations[self.action][self.direction]):
            self.frame_index = 0

        self.image = self.animations[self.action][self.direction][int(self.frame_index)]

    def collision(self, axis: str):
        # Change collider if statement and collider collision axis
        for obstacle in [entity for entity in self.collisions.sprites() if self.collider.colliderect(entity.rect)]:
            if axis == "x":
                if self.movement.x > 0:
                    self.collider.right = obstacle.rect.left
                if self.movement.x < 0:
                    self.collider.left = obstacle.rect.right
                self.x = self.collider.centerx
            if axis == "y":
                if self.movement.y > 0:
                    self.collider.bottom = obstacle.rect.top
                if self.movement.y < 0:
                    self.collider.top = obstacle.rect.bottom

                rect = self.rect
                rect.bottom = self.collider.bottom
                self.y = rect.centery

    def render(self, display: pygame.Surface, offset=(0, 0)):
        shadow_rect = self.shadow.get_rect()
        shadow_rect.centerx = self.x - offset[0]
        shadow_rect.centery = self.rect.bottom - 2 - offset[1]
        display.blit(self.shadow, shadow_rect)
        super().render(display, offset)
