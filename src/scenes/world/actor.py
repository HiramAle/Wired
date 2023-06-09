import random

import pygame
import src.utils.load as load
from engine.assets import Assets
from engine.time import Time
from src.scenes.world.sprite import Sprite
from engine.animation.animation import Animation
from engine.constants import Colors


class Emote(Sprite):
    def __init__(self, position: tuple, animation: Animation, name:str):
        super().__init__(position, animation.current_frame)
        self.animation = animation
        self.animation.loop = False
        self.name = name

    def update(self):
        self.animation.update()
        self.image = self.animation.current_frame


class Actor(Sprite):
    def __init__(self, position: tuple, sprite_sheet_path: str, collisions: list[pygame.Rect]):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        # TODO: Investigate why I put this where?
        animations = load.export_animation_frames(sprite_sheet)
        super().__init__(position, animations["idle"]["down"][0])
        self.collisions = collisions if collisions else []
        # Movement attributes
        self._position = pygame.Vector2(position)
        self.speed = 150
        self.movement = pygame.Vector2()
        # Animation attributes
        self.animations = animations
        self.direction = "down"
        self.action = "idle"
        self.frame_index = 0
        self.animation_speed = random.randint(9, 11)
        # Extra attributes
        self.shadow = Assets.images_actors["actor_shadow"]
        self.collider = pygame.Rect(0, 0, 28, 20)
        self.emote: Emote | None = None

    def draw_colliders(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        adjusted_collider = self.collider.copy()
        adjusted_collider.x -= offset.x
        adjusted_collider.y -= offset.y
        pygame.draw.rect(display, Colors.RED, adjusted_collider, 2)



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
        elif self.action == "walk":
            self.action = "idle"

    def move(self):
        if self.movement.magnitude() > 1:
            self.movement = self.movement.normalize()
        self.x += self.movement.x * self.speed * Time.dt
        self.collider.centerx = self.x
        self.collision("x")
        self.y += self.movement.y * self.speed * Time.dt
        self.collider.bottom = self.rect.bottom
        self.collision("y")

    def animate(self):
        self.frame_index += Time.dt * self.animation_speed
        if self.frame_index >= len(self.animations[self.action][self.direction]):
            self.frame_index = 0

        self.image = self.animations[self.action][self.direction][int(self.frame_index)]

    def collision(self, axis: str):
        # Change collider if statement and collider collision axis
        for obstacle in [collider for collider in self.collisions if self.collider.colliderect(collider)]:
            if axis == "x":
                if self.movement.x > 0:
                    self.collider.right = obstacle.left
                if self.movement.x < 0:
                    self.collider.left = obstacle.right
                self.x = self.collider.centerx
            if axis == "y":
                if self.movement.y > 0:
                    self.collider.bottom = obstacle.top
                if self.movement.y < 0:
                    self.collider.top = obstacle.bottom

                rect = self.rect
                rect.bottom = self.collider.bottom
                self.y = rect.centery

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.shadow:
            shadow_rect = self.shadow.get_rect()
            shadow_rect.centerx = self.x - offset.x
            shadow_rect.centery = self.rect.bottom - 2 - offset.y
            display.blit(self.shadow, shadow_rect)
        super().render(display, offset)
        if self.emote:
            self.emote.render(display, offset)
