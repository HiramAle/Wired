from __future__ import annotations
import sys
import pygame
from pygame.math import Vector2
from pygame import Surface, Rect, SRCALPHA
from pygame.transform import scale_by, flip, rotate


class Group:
    def __init__(self):
        self.__entities: list[Entity] = []

    @property
    def entities(self) -> list[Entity]:
        return self.__entities

    @property
    def entities_by_bottom(self) -> list[Entity]:
        return sorted(self.__entities, key=lambda entity: entity.rect.bottom)

    def add(self, *entities: Entity):
        for entity in entities:
            self.__entities.append(entity)

    def update(self, *args, **kwargs):
        for entity in self.entities:
            entity.update(*args, **kwargs)

    def render(self, surface: Surface, offset=Vector2(0, 0)):
        for entity in self.entities:
            if entity.image:
                rect = entity.rect
                rect.x += offset.x
                rect.y += offset.y
                surface.blit(entity.image, rect)
            entity.render(surface)

    def render_3d(self, surface: Surface, offset=Vector2(0, 0)):
        for entity in self.entities_by_bottom:
            if entity.image:
                rect = entity.rect
                rect.x += offset.x
                rect.y += offset.y
                surface.blit(entity.image, rect)
            entity.render(surface)


class Entity:
    def __init__(self, **kwargs) -> None:
        self.name = self.__class__.__name__.lower()
        self.enabled = True
        self.visible = True
        # ------------
        #  Transform
        # ------------
        self.__position = Vector2(0, 0)
        self.__scale = 1
        self.rotation = 0
        # ------------
        #   Renderer
        # ------------
        self.__image: Surface | None = None
        self.__opacity = 255
        self.__flip = [False, False]
        # ------------
        #   Collider
        # ------------
        self.collider: Rect | None = None
        self.layer = 0

    @property
    def position(self) -> Vector2:
        return self.__position

    @position.setter
    def position(self, value: tuple[float, float]) -> None:
        self.__position.x, self.__position.y = value

    @property
    def image(self) -> Surface:
        return self.__image

    @image.setter
    def image(self, value: Surface):
        self.__image = value
        self.__apply_transform()

    def __apply_transform(self):
        if self.scale != 1:
            self.__image = scale_by(self.__image, self.scale)
        if self.rotation != 0:
            self.__image = rotate(self.__image, self.rotation)
        if any(self.__flip):
            self.__image = flip(self.__image, *self.__flip)
        if self.__opacity != 255:
            self.__image.set_alpha(self.__opacity)

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        self.__scale: value
        self.__apply_transform()

    @property
    def rect(self) -> Rect:
        return self.__image.get_rect(center=self.position)

    def update(self, *args, **kwargs):
        ...

    def render(self, surface: Surface, offset=(0, 0)):
        ...
