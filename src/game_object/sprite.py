from __future__ import annotations
import pygame

from src.game_object.game_object import GameObject


class Sprite(GameObject):
    def __init__(self, name: str, position: tuple[float, float], image: pygame.Surface, *groups):
        super().__init__(name, position, image)
        self.groups = groups if groups else []

    def render(self, display: pygame.Surface, special_flags=None):
        if not self.active:
            return

        display.blit(self.image, self.rect, special_flags=special_flags)

    def add(self, *groups: SpriteGroup):
        for group in groups:
            if self not in group.sprites:
                self.groups.append(group)
                group.add(self)

    def kill(self):
        for group in self.groups:
            group.remove(self)


class SpriteGroup:
    def __init__(self):
        self._sprites: list[Sprite] = []

    @property
    def sprites(self):
        return sorted(self._sprites, key=lambda sprite: sprite.layer)

    def add(self, *sprites: Sprite):
        for sprite in sprites:
            self._sprites.append(sprite)

    def remove(self, sprite: Sprite):
        if sprite in self._sprites:
            self._sprites.remove(sprite)

    def get_interactive_sprites(self) -> list[Sprite]:
        return [sprite for sprite in self.sprites if sprite.interactive]
