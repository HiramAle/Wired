import random
import pygame
from src.new_objects.entity import Entity, Group
import json


def export_animation_frames(sprite_sheet: pygame.Surface) -> dict:
    sprite_height = 48
    sprite_width = 32
    crop_height = 64
    crop_width = 32
    animation_frames = {}
    with open("../../data/character_creation/animation_frames_data.json", "r") as file:
        animation_frames = json.load(file)

    animations = {action: {direction: [] for direction in value.keys()} for action, value in animation_frames.items()}
    row = 0
    column = 0
    for animation, directions in animation_frames.items():
        for direction, frames in directions.items():
            for frame in range(frames):
                x_crop = column * crop_width
                y_crop = 16 + (row * crop_height)
                image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                image.blit(sprite_sheet, (0, 0), (x_crop, y_crop, crop_width, crop_height))
                animations[animation][direction].append(image)
                column += 1
        row += 1
        column = 0
    return animations


class Tile(Entity):
    def __init__(self):
        super().__init__()

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(topleft=self.position)


class Obstacle(Tile):
    def __init__(self, collider: pygame.Rect):
        super().__init__()
        self.collider = collider


class Actor(Entity):
    def __init__(self, position: tuple, obstacles: Group):
        super().__init__()
        sheet = pygame.image.load("sprite_sheet.png").convert_alpha()
        self.position = position
        self.animations = export_animation_frames(sheet)
        self.image = self.animations["idle"]["down"][0]
        self.speed = 150
        self.obstacles = obstacles
        self.movement = pygame.Vector2(0, 0)
        self.action = "idle"
        self.direction = "down"
        self.collider = pygame.Rect(0, 0, 20, 20)
        self.frame_index = random.randint(0, len(self.animations["idle"]) - 1)
        print(self.frame_index)
        self.animation_speed = 10

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
            self.action = "idle"

    def move(self, dt: float):
        if self.movement.magnitude() > 1:
            self.movement = self.movement.normalize()
        self.position.x += self.movement.x * self.speed * dt
        self.collider.centerx = self.position.x
        self.collision("x")
        self.position.y += self.movement.y * self.speed * dt
        self.collider.centery = self.position.y
        self.collision("y")

    def animate(self, dt: float):
        self.frame_index += dt * self.animation_speed
        if self.frame_index >= len(self.animations[self.action][self.direction]):
            self.frame_index = 0

        self.image = self.animations[self.action][self.direction][int(self.frame_index)]

    def collision(self, axis: str):
        # Change collider if statement and collider collision axis
        for obstacle in [entity for entity in self.obstacles.entities if self.collider.colliderect(entity.collider)]:
            obstacle: Obstacle
            if axis == "x":
                if self.movement.x > 0:
                    self.collider.right = obstacle.collider.left
                if self.movement.x < 0:
                    self.collider.left = obstacle.collider.right
                self.position.x = self.collider.centerx
            if axis == "y":
                if self.movement.y > 0:
                    self.collider.bottom = obstacle.collider.top
                if self.movement.y < 0:
                    self.collider.top = obstacle.collider.bottom
                self.position.y = self.collider.centery

    def update(self, *args, **kwargs):
        print(f"{self.action}_{self.direction} at {self.movement.magnitude()}")


class NPC(Actor):
    def __init__(self, position: tuple, obstacles: Group):
        super().__init__(position, obstacles)
        self.path_index = 0
        self.path = [(500, 200), (500, 800), (879, 814), (880, 893), (1189, 891)]
        self.target = pygame.Vector2(0, 0)

    def pathing(self):
        self.movement.x, self.movement.y = 0, 0
        if self.path_index >= len(self.path):
            return
        self.target.x, self.target.y = self.path[self.path_index]
        self.movement = self.target - self.position

        if self.movement.magnitude() <= 5:
            self.path_index += 1

    def update(self, *args, **kwargs):
        self.pathing()
        self.move(**kwargs)
        self.update_status()
        self.animate(**kwargs)
        print(f"{self.action}_{self.direction} at {self.movement.magnitude()}")


class Player(Actor):
    def __init__(self, position: tuple, obstacles: Group):
        super().__init__(position, obstacles)

    def set_movement(self):
        self.movement.x, self.movement.y = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x = - 1
            self.direction = "left"
        if keys[pygame.K_d]:
            self.movement.x = 1
            self.direction = "right"
        if keys[pygame.K_w]:
            self.movement.y = - 1
            self.direction = "up"
        if keys[pygame.K_s]:
            self.movement.y = 1
            self.direction = "down"

        if self.movement.magnitude() > 0:
            self.movement = self.movement.normalize()

    def input(self):
        self.movement.x, self.movement.y = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x = - 1
        if keys[pygame.K_d]:
            self.movement.x = 1
        if keys[pygame.K_w]:
            self.movement.y = - 1
        if keys[pygame.K_s]:
            self.movement.y = 1

    def update(self, *args, **kwargs):
        self.input()
        self.move(**kwargs)
        self.update_status()
        self.animate(**kwargs)
