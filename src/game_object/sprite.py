from __future__ import annotations
import pygame
from typing import Optional
from src.game_object.game_object import GameObject
from src.game_object.components import Render


class Sprite(GameObject, Render):
    """
    A class representing a graphical Sprite that can be drawn on a surface and can be added to a SpriteGroup.
    """

    def __init__(self, name: str, position: tuple[float, float], image: pygame.Surface, *groups, **kwargs):
        """
        Initializes a new Sprite object.
        :param name: The name of the sprite.
        :param position: The x and y coordinates of the sprite.
        :param image: The sprite's image.
        :param groups: The groups that the sprite belongs to.
        """
        GameObject.__init__(self, name, position, image.get_size())
        Render.__init__(self, image)
        self.groups: list[SpriteGroup] = []
        self._flags = 0
        if groups:
            self.add(*groups)

        for key, value in kwargs.items():
            match key:
                case "flags":
                    self._flags = value
                case "layer":
                    self.layer = value
                case "centered":
                    self.centered = value
                case "scale":
                    self.scale = value

    # @Render.image.setter
    # def image(self, new_image: pygame.Surface):
    #     Render.image.setter = new_image
    #     self._source_image = new_image
    #     self._image = self._source_image.copy()

    @property
    def rect(self) -> pygame.Rect:
        if self.centered:
            return self.image.get_rect(center=self.position)
        else:
            return self.image.get_rect(topleft=self.position)

    def render(self, display: pygame.Surface):
        """
        Renders the sprite onto the display surface.
        :param display: The surface to render the sprite on.
        :param special_flags: Pygame special rendering flags, such as pygame.BLEND_RGBA_ADD.
        """
        display.blit(self.image, self.rect, special_flags=self._flags)

    def add(self, *groups: SpriteGroup):
        """
        Adds the sprite to the specified sprite groups.
        :param groups: The sprite groups to add the sprite to.
        """
        for group in groups:
            if self not in group.sprites:
                self.groups.append(group)
                group.add(self)

    def kill(self):
        """
        Removes the sprite from all sprite groups.
        """
        for group in self.groups:
            group.remove(self)


class SpriteGroup:
    """
    A class for grouping Sprites together and updating/rendering them.
    """

    def __init__(self):
        """
        Initializes a new Sprite object.
        """
        self._sprites: list[Sprite] = []

    @property
    def sprites(self):
        return sorted(self._sprites, key=lambda sprite: sprite.layer)

    def add(self, *sprites: Sprite):
        """
        Add one or more Sprites to the group.
        :param sprites: One or more Sprite instances.
        """
        for sprite in sprites:
            self._sprites.append(sprite)

    def remove(self, sprite: Sprite):
        """
        Remove a Sprite from the group.
        :param sprite: The Sprite instance to remove.
        """
        if sprite in self._sprites:
            self._sprites.remove(sprite)

    def update(self):
        """
        Call the update method of each Sprite in the group.
        """
        for sprite in self.sprites:
            if not sprite.active:
                continue
            sprite.update()

    def render(self, display: pygame.Surface):
        """
        Call the render method of each Sprite in the group.
        :param display: The surface to render the Sprites onto.
        """
        for sprite in self.sprites:
            if not sprite.active:
                continue
            sprite.render(display)
