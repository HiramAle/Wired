from pygame import Vector2


class GameObject:
    def __init__(self, position=(0, 0)):
        self._position = Vector2(position)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: tuple[float, float]) -> None:
        self._position.x, self._position.y = value

    @property
    def x(self) -> float:
        return self._position.x

    @x.setter
    def x(self, value: float) -> None:
        self._position.x = value

    @property
    def y(self) -> float:
        return self._position.y

    @y.setter
    def y(self, value: float) -> None:
        self._position.y = value
