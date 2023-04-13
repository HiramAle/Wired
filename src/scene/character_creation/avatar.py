import pygame
import src.engine.time as time
import src.engine.assets as assets
from src.game_object.sprite import Sprite
from src.components.animation import Animation


class Avatar(Sprite, Animation):
    def __init__(self, *groups):
        super().__init__("avatar", (411, 234), pygame.Surface((64, 128), pygame.SRCALPHA), *groups)
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

    def __repr__(self):
        return f"{self.outfit}"

    def play(self):
        self._frame_index += self.animation_speed * time.dt
        if self._frame_index > self.last_index:
            self._frame_index = 0

    def next_outfit(self):
        self.outfit += 1
        self.outfit_color = 0
        if self.outfit not in assets.outfits:
            self.outfit = 0

    def previous_outfit(self):
        self.outfit -= 1
        self.outfit_color = 0
        if self.outfit not in assets.outfits:
            self.outfit = len(assets.outfits) - 1

    def next_hairstyle(self):
        self.hairstyle += 1
        self.hairstyle_color = 0
        if self.hairstyle not in assets.hairstyles:
            self.hairstyle = 0

    def previous_hairstyle(self):
        self.hairstyle -= 1
        self.hairstyle_color = 0
        if self.hairstyle not in assets.hairstyles:
            self.hairstyle = len(assets.hairstyles) - 1

    @property
    def body_frame(self) -> pygame.Surface:
        return assets.bodies[self.body][self.direction][self.frame_index]

    @property
    def eyes_frame(self) -> pygame.Surface:
        return assets.eyes[self.eyes][self.direction][self.frame_index]

    @property
    def outfit_frame(self) -> pygame.Surface:
        return assets.outfits[self.outfit][self.outfit_color][self.direction][self.frame_index]

    @property
    def hairstyle_frame(self) -> pygame.Surface:
        return assets.hairstyles[self.hairstyle][self.hairstyle_color][self.direction][self.frame_index]

    @property
    def image(self) -> pygame.Surface:
        image = self._image.copy()
        image.blit(pygame.transform.scale(self.body_frame, (64, 128)), (0, 0))
        image.blit(pygame.transform.scale(self.outfit_frame, (64, 128)), (0, 0))
        image.blit(pygame.transform.scale(self.hairstyle_frame, (64, 128)), (0, 0))
        image.blit(pygame.transform.scale(self.eyes_frame, (64, 128)), (0, 0))
        return image

    @property
    def frame_index(self) -> int:
        return int(self._frame_index)
