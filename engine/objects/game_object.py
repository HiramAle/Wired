import pygame


class GameObject:
    """
    Represents a game object.
    """

    def __init__(self, name="objects", position=(0, 0)):
        """
        Initializes a new GameObject.
        :param name: The name of the object. Default is GameObject.
        :param position: The initial position of the game object. Default is (0, 0).
        """
        self.name = name
        self.__position = pygame.math.Vector2(position)
        self.active = True

    def internal_update(self, *args, **kwargs):
        if not self.active:
            return
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        ...

    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    @position.setter
    def position(self, value):
        if isinstance(value, tuple):
            self.__position = pygame.Vector2(*value)
        elif isinstance(value, pygame.Vector2):
            self.__position = value

    @property
    def x(self) -> float:
        return self.__position.x

    @x.setter
    def x(self, value: float):
        self.__position.x = value

    @property
    def y(self) -> float:
        return self.__position.y

    @y.setter
    def y(self, value: float):
        self.__position.y = value
