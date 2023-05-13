import pygame


class Position:
    """
    Component that represents a 2D position, with a layer attribute.
    """

    def __init__(self, position: tuple[int | float, int | float]):
        """
        Initializes a new Position objects.
        :param position: The (x, y) coordinates of the position.
        """
        self._position = pygame.math.Vector2(position)

    @property
    def x(self) -> int | float:
        return self._position.x

    @property
    def y(self) -> int | float:
        return self._position.y

    @property
    def position(self) -> tuple[int | float, int | float]:
        return self.x, self.y

    @property
    def position_vector(self) -> pygame.math.Vector2:
        return self._position

    @x.setter
    def x(self, value: int | float) -> None:
        self._position.x = value

    @y.setter
    def y(self, value: int | float) -> None:
        self._position.y = value

    @position.setter
    def position(self, value: tuple[int | float, int | float]) -> None:
        self.x, self.y = value

    @position_vector.setter
    def position_vector(self, value: pygame.Vector2) -> None:
        self._position = value
