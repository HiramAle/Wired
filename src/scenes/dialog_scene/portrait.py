import pygame
from engine.assets import Assets
from engine.time import Time

from engine.objects.sprite import Sprite


class Portrait(Sprite):
    def __init__(self, npc: str):
        super().__init__((178, 295), pygame.Surface((64, 64), pygame.SRCALPHA))
        self.frames = Assets.portrait_frames[npc]["talk"]
        self.animation_speed = 10
        self.frame_index = 0

    def update(self, *args, **kwargs):
        self.frame_index += self.animation_speed * Time.dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
