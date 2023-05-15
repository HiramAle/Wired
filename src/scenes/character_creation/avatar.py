import random
import pygame
from engine.time import Time
from engine.assets import Assets
from engine.objects.sprite import Sprite
from src.utils.load import save_sprite_sheet


class Avatar(Sprite):
    def __init__(self, *groups):
        super().__init__((445, 225), pygame.Surface((64, 128), pygame.SRCALPHA), *groups)
        self._frame_index = 0
        self.direction = "down"
        self.animation_speed = 8
        self.last_index = 5
        # Character indexes
        self.body = 0
        self.eyes = 0
        self.hairstyle = 0
        self.hairstyle_color = 0
        self.outfit = 0
        self.outfit_color = 0

    def randomize(self):
        self.hairstyle = random.choice(range(len(Assets.hairstyles) - 1))
        self.outfit = random.choice(range(len(Assets.outfits) - 1))
        self.body = random.choice(range(len(Assets.bodies) - 1))
        self.eyes = random.choice(range(len(Assets.eyes) - 1))

    def play(self):
        self._frame_index += self.animation_speed * Time.dt
        if self._frame_index > self.last_index:
            self._frame_index = 0
        self.update_image()

    def next_outfit(self):
        self.outfit += 1
        self.outfit_color = 0
        if self.outfit not in Assets.outfits:
            self.outfit = 0

    def previous_outfit(self):
        self.outfit -= 1
        self.outfit_color = 0
        if self.outfit not in Assets.outfits:
            self.outfit = len(Assets.outfits) - 1

    def next_hairstyle(self):
        self.hairstyle += 1
        self.hairstyle_color = 0
        if self.hairstyle not in Assets.hairstyles:
            self.hairstyle = 0

    def previous_hairstyle(self):
        self.hairstyle -= 1
        self.hairstyle_color = 0
        if self.hairstyle not in Assets.hairstyles:
            self.hairstyle = len(Assets.hairstyles) - 1

    @property
    def body_frame(self) -> pygame.Surface:
        return Assets.bodies[self.body][self.direction][self.frame_index]

    @property
    def eyes_frame(self) -> pygame.Surface:
        return Assets.eyes[self.eyes][self.direction][self.frame_index]

    @property
    def outfit_frame(self) -> pygame.Surface:
        return Assets.outfits[self.outfit][self.outfit_color][self.direction][self.frame_index]

    @property
    def hairstyle_frame(self) -> pygame.Surface:
        return Assets.hairstyles[self.hairstyle][self.hairstyle_color][self.direction][self.frame_index]

    def save_character(self):
        save_sprite_sheet(self.body, self.eyes, (self.hairstyle, self.hairstyle_color),
                          (self.outfit, self.outfit_color))

    def update_image(self):
        self.image = pygame.Surface((64, 128), pygame.SRCALPHA)
        self.image.blit(pygame.transform.scale(self.body_frame, (64, 128)), (0, 0))
        self.image.blit(pygame.transform.scale(self.outfit_frame, (64, 128)), (0, 0))
        self.image.blit(pygame.transform.scale(self.hairstyle_frame, (64, 128)), (0, 0))
        self.image.blit(pygame.transform.scale(self.eyes_frame, (64, 128)), (0, 0))

    @property
    def frame_index(self) -> int:
        return int(self._frame_index)
