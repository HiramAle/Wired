import pygame
import src.engine.input as input
from src.components.position import Position

object_id = 0


class GameObject(Position):
    """
    Represents a game object.
    """

    def __init__(self, name="game_object", position=(0, 0), size=(16, 16)):
        """
        Initializes a new GameObject.
        :param name: The name of the object. Default is GameObject.
        :param position: The initial position of the game object. Default is (0, 0).
        """
        super().__init__(position)
        self.id = object_id + 1
        self.name = name
        self._centered = True
        self.active = True
        self.interactive = False
        self.size = size

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, value: int | float):
        self.size[0] = value

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, value: int | float):
        self.size[1] = value

    @property
    def rect(self) -> pygame.Rect:
        rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        if self._centered:
            rect.center = self.position
        else:
            rect.topleft = self.position
        return rect

    @property
    def centered(self) -> bool:
        return self._centered

    @centered.setter
    def centered(self, value: bool):
        self._centered = value

    @property
    def hovered(self) -> bool:
        if self.rect.collidepoint(input.mouse.position):
            return True
        return False

    @property
    def clicked(self) -> bool:
        if self.hovered and input.mouse.buttons["left"]:
            return True
        return False

    def update(self, *args, **kwargs):
        ...
