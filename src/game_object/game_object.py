import pygame
import src.engine.input as input
from src.game_object.components import Position, Render


class GameObject(Position, Render):
    """
    Represents a game object.
    """

    def __init__(self, name="GameObject", position=(0, 0), image=pygame.Surface((0, 0))):
        """
        Initializes a new GameObject.
        :param name: The name of the object. Default is GameObject.
        :param position: The initial position of the game object. Default is (0, 0).
        :param image: The image of the game object. Default is an empty surface with size (0, 0).
        """
        Position.__init__(self, position)
        Render.__init__(self, image)
        self.name = name
        self._centered = True
        self._visible = True
        self.active = True
        self.interactive = False

    @property
    def rect(self) -> pygame.Rect:
        if self._centered:
            return self.image.get_rect(center=self.position)
        else:
            return self.image.get_rect(topleft=self.position)

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
