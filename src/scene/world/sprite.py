import enum

import pygame
import src.engine.input as game_input
from src.scene.world.game_object import GameObject


class Sprite(GameObject):
    def __init__(self, position: tuple, image: pygame.Surface):
        super().__init__(position)
        self.image = image
        self._sort_point = "bottom"

    @property
    def sort_point(self) -> float:
        if self._sort_point == "bottom":
            return self.rect.bottom
        else:
            return self.rect.centery

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)) -> None:
        rect = self.rect
        rect.x -= offset.x
        rect.y -= offset.y
        display.blit(self.image, rect)

    def update(self):
        ...

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(center=self._position)

    def hovered(self, offset: pygame.Vector2) -> bool:
        mouse = pygame.Vector2(game_input.mouse.position) + offset
        if self.rect.collidepoint(mouse):
            return True
        return False

    def clicked(self, offset: pygame.Vector2) -> bool:
        mouse = pygame.Vector2(game_input.mouse.position) + offset
        if self.rect.collidepoint(mouse) and game_input.mouse.buttons["left"]:
            return True
        return False
