import pygame
import src.engine.input as input
from src.game_object.components import Position, Render


class GameObject(Position):
    """
    Represents a game object.
    """

    def __init__(self, name="GameObject", position=(0, 0), size=(16, 16)):
        """
        Initializes a new GameObject.
        :param name: The name of the object. Default is GameObject.
        :param position: The initial position of the game object. Default is (0, 0).
        """
        super().__init__(position)
        self.name = name
        self._centered = True
        self._visible = True
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
        rect = pygame.Rect(0, 0, self.size)
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
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value

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

    def update(self):
        ...

    def activate(self):
        """
        Activates the object.
        """
        if not self.active:
            self.active = True

    def deactivate(self):
        """
        Deactivates the object.
        """
        if self.active:
            self.active = False


