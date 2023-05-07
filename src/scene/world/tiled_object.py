import pygame
from src.scene.world.sprite import Sprite


class TiledObject(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, colliders: list[pygame.Rect], sort_by_center):
        super().__init__(position, image)
        self._colliders = colliders
        self._sort_point = sort_by_center

    def __repr__(self):
        return f"TiledObject {self.position}"

    @property
    def colliders(self) -> list[pygame.Rect]:
        colliders_ = []
        for collider in self._colliders:
            col = collider.copy()
            col.x += self.x
            col.y += self.y
            colliders_.append(col)
        return colliders_

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(topleft=self._position)
