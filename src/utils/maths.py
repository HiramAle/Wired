import pygame
import math


def sin_wave(value: int | float, distance: int, speed: int, time=1280) -> int:
    time = pygame.time.get_ticks() % time
    return int(value + math.sin(time / speed) * distance)
