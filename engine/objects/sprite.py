from __future__ import annotations

import copy

import pygame
from engine.input import Input
from engine.objects.game_object import GameObject
from enum import Enum
from typing import Optional


class Sprite(GameObject):
    """
    A class representing a graphical Sprite that can be drawn on a surface and can be added to a SpriteGroup.
    """

    class Pivot(Enum):
        CENTER = 0
        TOP_LEFT = 1
        MID_BOTTOM = 2

    def __init__(self, position=(0, 0), image: pygame.Surface = None, *groups, **kwargs):
        """
        Initializes a new Sprite object.
        :param name: The name of the sprite.
        :param position: The x and y coordinates of the sprite.
        :param image: The sprite's image.
        :param groups: The groups that the sprite belongs to.
        """
        super().__init__(self.__class__.__name__, position)
        self.__groups: list[SpriteGroup] = []
        self.__image: pygame.Surface | None = image
        self.__opacity = 255
        self.__flip = [False, False]
        self.flags = 0
        self.layer = 0
        self.scale = 1
        self.pivot = self.Pivot.CENTER
        self.collider_pivot = self.Pivot.CENTER
        self.__collider = self.rect

        if groups:
            self.add(*groups)

        for key, val in kwargs.items():
            if key in ["flags", "layer", "centered", "scale", "opacity"] and hasattr(self, key):
                setattr(self, key, val)

    @property
    def centered(self) -> bool:
        return self.pivot == self.Pivot.CENTER

    @centered.setter
    def centered(self, value: bool):
        if value:
            self.pivot = self.Pivot.CENTER
        else:
            self.pivot = self.Pivot.TOP_LEFT

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface):
        image = value
        if self.__scale != 1:
            image = pygame.transform.scale_by(image, self.__scale)
        if self.__opacity != 255:
            image.set_alpha(self.__opacity)
        if any(self.__flip):
            image = pygame.transform.flip(image, *self.__flip)
        self.__image = image

    def __repr__(self):
        return f"Sprite({self.name},{self.position} ,{self.image})"

    def activate(self):
        if self.active:
            return
        self.active = True

    def deactivate(self):
        if not self.active:
            return
        self.active = False

    def add_internal(self, group: SpriteGroup):
        """
        Adds the sprite to a sprite group.
        :param group: The sprite group to add the sprite to.
        """
        self.__groups.append(group)

    def remove_internal(self, group: SpriteGroup):
        """
        Removes the sprite from a sprite group.
        :param group: The sprite group to remove the sprite from.
        """
        self.__groups.remove(group)

    def add(self, *groups: SpriteGroup):
        """
        Adds the sprite to the specified sprite groups.
        :param groups: The sprite groups to add the sprite to.
        """
        for group in groups:
            if not group.has(self):
                group.add_internal(self)
                self.add_internal(group)

    def remove(self, *groups: SpriteGroup):
        """
        Removes the sprite from the specified sprite groups.
        :param groups: The sprite groups to remove the sprite from.
        """
        for group in groups:
            if group.has(self):
                group.remove_internal(self)
                self.remove_internal(group)

    def kill(self):
        """
        Removes the sprite from all sprite groups.
        """
        for group in self.__groups:
            group.remove_internal(self)

    def groups(self) -> list[SpriteGroup]:
        """
        Returns the sprite groups that the sprite belongs to.
        :return: A list of sprite groups that the sprite belongs to.
        """
        return self.__groups.copy()

    @property
    def hovered(self) -> bool:
        if not self.active:
            return False
        if self.rect.collidepoint(Input.mouse.position):
            return True
        return False

    @property
    def clicked(self) -> bool:
        if not self.active:
            return False
        if not self.hovered:
            return False
        if Input.mouse.buttons["left"]:
            return True
        return False

    @property
    def rect(self) -> pygame.Rect:
        match self.pivot:
            case self.Pivot.CENTER:
                return self.image.get_rect(center=self.position)
            case self.Pivot.TOP_LEFT:
                return self.image.get_rect(topleft=self.position)
            case self.Pivot.MID_BOTTOM:
                return self.image.get_rect(midbottom=self.position)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        """
        Renders the sprite onto the display surface.
        :param display: The surface to render the sprite on.
        :param offset:
        """
        if not self.active or not self.image:
            return
        rect = self.rect
        rect.x += offset.x
        rect.y += offset.y
        display.blit(self.image, rect, special_flags=self.flags)

    @property
    def top_left(self) -> tuple[float, float]:
        return self.rect.topleft

    @top_left.setter
    def top_left(self, value: tuple[float, float]):
        rect = self.rect
        rect.topleft = value
        self.position = rect.center

    @property
    def center(self) -> tuple[float, float]:
        return self.rect.center

    @center.setter
    def center(self, value: tuple[float, float]):
        pass

    @property
    def center_x(self) -> float:
        return self.rect.centerx

    @center_x.setter
    def center_x(self, value):
        pass

    @property
    def flip(self) -> tuple[bool, bool]:
        return self.__flip[0], self.__flip[1]

    @flip.setter
    def flip(self, value: tuple[bool, bool]):
        self.__flip = value
        self.image = pygame.transform.flip(self.image, value[0], value[1])

    @property
    def opacity(self) -> int:
        return self.__opacity

    @opacity.setter
    def opacity(self, value: int):
        if value < 0 or value > 255:
            raise ValueError("Opacity factor must be greater than zero and lesser than 255.")
        self.__opacity = value
        self.image.set_alpha(value)

    @property
    def scale(self) -> int:
        return self.__scale

    @scale.setter
    def scale(self, value: int):
        if value <= 0:
            raise ValueError("Scale factor must be greater than zero.")
        self.__scale = value
        self.image = pygame.transform.scale_by(self.image, value)


class SpriteGroup:
    """
    A class for grouping Sprites together and updating/rendering them.
    """

    def __init__(self, *sprites: Sprite):
        """
        Initializes a new SpriteGroup object.
        """
        self._sprites: list[Sprite] = []
        if sprites:
            self.add(*sprites)

    def __repr__(self):
        return f"SpriteGroup({len(self._sprites)})"

    def add_internal(self, sprite: Sprite):
        """
        Adds a Sprite to the group.
        :param sprite: The Sprite instance to add to the group.
        """
        self._sprites.append(sprite)

    def remove_internal(self, sprite: Sprite):
        """
        Removes a Sprite from the group.
        :param sprite: The Sprite instance to remove from the group.
        """
        self._sprites.remove(sprite)

    def add(self, *sprites: Sprite):
        """
        Add one or more Sprites to the group.
        :param sprites: One or more Sprite instances.
        """
        for sprite in sprites:
            if not self.has(sprite):
                self._sprites.append(sprite)
                sprite.add_internal(self)

    def remove(self, *sprites: Sprite):
        """
        Remove a Sprite from the group.
        :param sprites: The Sprite instances to remove.
        """
        for sprite in sprites:
            if self.has(sprite):
                self._sprites.remove(sprite)
                sprite.remove_internal(self)

    def has(self, sprite: Sprite) -> bool:
        """
        Returns True if the given Sprite is in the group, False otherwise.
        :param sprite: The Sprite instance to check.
        :return: True if the Sprite is in the group, False otherwise.
        """
        return sprite in self._sprites

    def sprites(self) -> list[Sprite]:
        """
        Returns a list of Sprites in the group.
        :return: A list of Sprites in the group.
        """
        return sorted(self._sprites, key=lambda sprite_: sprite_.layer)

    def update(self, *args, **kwargs):
        """
        Call the update method of each Sprite in the group.
        """
        for sprite in self.sprites():
            if not sprite.active:
                continue
            sprite.update(*args, **kwargs)

    def render(self, display: pygame.Surface, offset=pygame.Vector2):
        """
        Call the render method of each Sprite in the group.
        :param display: The surface to render the Sprites onto.
        :param offset: The position offset of the group from the display surface origin, defaults to (0, 0).
        """
        for sprite in self.sprites():
            if not sprite.active:
                continue
            sprite.render(display)

    def empty(self):
        for sprite in self.sprites():
            self.remove_internal(sprite)
            sprite.remove_internal(self)
