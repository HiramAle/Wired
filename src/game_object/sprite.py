from __future__ import annotations
import pygame
from src.game_object.game_object import GameObject
from src.components.render import Render


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
        self.__groups: list[SpriteGroup] = []
        self._flags = 0
        self._layer = 0
        self.active = True

        if groups:
            self.add(*groups)

        for key, val in kwargs.items():
            if key in ["flags", "layer", "centered", "scale"] and hasattr(self, key):
                setattr(self, key, val)

    def activate(self):
        if not self.active:
            self.active = True

    def deactivate(self):
        if self.active:
            self.active = False

    @property
    def layer(self) -> int:
        return self._layer

    @layer.setter
    def layer(self, value: int) -> None:
        self._layer = value

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
            group.remove(self)

    def groups(self) -> list[SpriteGroup]:
        """
        Returns the sprite groups that the sprite belongs to.
        :return: A list of sprite groups that the sprite belongs to.
        """
        return self.__groups.copy()

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value: int):
        self._flags = value

    @property
    def rect(self) -> pygame.Rect:
        if self.centered:
            return self.image.get_rect(center=self.position)
        else:
            return self.image.get_rect(topleft=self.position)

    def __repr__(self):
        return self.name

    def render(self, display: pygame.Surface, offset=(0, 0)):
        """
        Renders the sprite onto the display surface.
        :param display: The surface to render the sprite on.
        :param offset: Pygame special rendering flags, such as pygame.BLEND_RGBA_ADD.
        """
        rect = self.rect
        rect.centerx -= offset[0]
        rect.centery -= offset[1]
        display.blit(self.image, rect, special_flags=self.flags)


class SpriteGroup:
    """
    A class for grouping Sprites together and updating/rendering them.
    """

    def __init__(self, *sprites: Sprite):
        """
        Initializes a new SpriteGroup object.
        """
        self.__sprites: list[Sprite] = []
        if sprites:
            self.add(*sprites)

    def add_internal(self, sprite: Sprite):
        """
        Adds a Sprite to the group.
        :param sprite: The Sprite instance to add to the group.
        """
        self.__sprites.append(sprite)

    def remove_internal(self, sprite: Sprite):
        """
        Removes a Sprite from the group.
        :param sprite: The Sprite instance to remove from the group.
        """
        self.__sprites.remove(sprite)

    def add(self, *sprites: Sprite):
        """
        Add one or more Sprites to the group.
        :param sprites: One or more Sprite instances.
        """
        for sprite in sprites:
            if not self.has(sprite):
                self.__sprites.append(sprite)
                sprite.add_internal(self)

    def remove(self, *sprites: Sprite):
        """
        Remove a Sprite from the group.
        :param sprites: The Sprite instances to remove.
        """
        for sprite in sprites:
            if self.has(sprite):
                self.__sprites.remove(sprite)
                sprite.remove_internal(self)

    def has(self, sprite: Sprite) -> bool:
        """
        Returns True if the given Sprite is in the group, False otherwise.
        :param sprite: The Sprite instance to check.
        :return: True if the Sprite is in the group, False otherwise.
        """
        return sprite in self.__sprites

    def sprites(self) -> list[Sprite]:
        """
        Returns a list of Sprites in the group.
        :return: A list of Sprites in the group.
        """
        return sorted(self.__sprites, key=lambda sprite_: sprite_.layer)

    def update(self, *args, **kwargs):
        """
        Call the update method of each Sprite in the group.
        """
        for sprite in self.sprites():
            if not sprite.active:
                continue
            sprite.update(*args, **kwargs)

    def render(self, display: pygame.Surface, offset=(0, 0)):
        """
        Call the render method of each Sprite in the group.
        :param display: The surface to render the Sprites onto.
        :param offset: The position offset of the group from the display surface origin, defaults to (0, 0).
        """
        for sprite in self.sprites():
            if not sprite.active:
                continue
            sprite.render(display, offset)

    def empty(self):
        for sprite in self.__sprites:
            sprite.kill()
