import pygame
import src.engine.time as time


class Position:
    """
    Component that represents a 2D position, with a layer attribute.
    """

    def __init__(self, position: tuple[int | float, int | float]):
        """
        Initializes a new Position game_object.
        :param position: The (x, y) coordinates of the position.
        """
        self._position = pygame.math.Vector2(position)
        self._layer = 0

    @property
    def x(self) -> int | float:
        return self._position.x

    @property
    def y(self) -> int | float:
        return self._position.y

    @property
    def layer(self) -> int:
        return self._layer

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

    @layer.setter
    def layer(self, value: int) -> None:
        self._layer = value

    @position.setter
    def position(self, value: tuple[int | float, int | float]) -> None:
        self.x, self.y = value

    @position_vector.setter
    def position_vector(self, value: pygame.Vector2) -> None:
        self._position = value


class Render:
    """
    Component that represents an Object with render capabilities.
    """

    def __init__(self, image: pygame.Surface):
        """
        Initializes a new Render object.
        :param image: The image to render.
        """
        self._source_image = image
        self._image = self._source_image.copy()
        self._opacity = 255
        self._scale = 1
        self._flip = [False, False]

    @property
    def image(self) -> pygame.Surface:
        return self._image

    @image.setter
    def image(self, new_image: pygame.Surface):
        self._source_image = new_image
        self._image = self._source_image.copy()

    @property
    def scale(self) -> int:
        return self._scale

    @scale.setter
    def scale(self, new_scale: int):
        if new_scale <= 0:
            raise ValueError("Scale factor must be greater than zero.")
        self._scale = new_scale
        self._image = pygame.transform.scale_by(self._image, new_scale)

    @property
    def flip(self) -> tuple[bool, bool]:
        return self._flip[0], self._flip[1]

    @flip.setter
    def flip(self, value: tuple[bool, bool]):
        self._flip = value
        self._image = pygame.transform.flip(self._image, value[0], value[1])

    @property
    def opacity(self) -> int:
        return self._opacity

    @opacity.setter
    def opacity(self, new_opacity: int):
        if new_opacity <= 0 or new_opacity > 255:
            raise ValueError("Opacity factor must be greater than zero and lesser than 255")
        self._opacity = new_opacity
        self._image.set_alpha(new_opacity)




class Animation:
    """
    Component that represents that represent an animation made up of multiple frames.
    """

    def __init__(self, data: list):
        """
        Initializes a new Animation object.
        :param frames: A list of Pygame Surfaces representing the frames of the animation.
        """
        self.data = data[1]
        self.frames = data[0]
        self.actual_frame = 0
        self.speed = self.data["speed"]

    @property
    def frame(self) -> pygame.Surface:
        return self.frames[int(self.actual_frame)]

    def play(self):
        """
        Plays the animation by incrementing the actual_frame attribute based on the speed and the delta time. If the
        actual_frame attribute exceeds the number of frames, it is reset to 0.
        """
        self.actual_frame += self.speed * time.dt
        if self.actual_frame >= len(self.frames):
            self.actual_frame = 0
