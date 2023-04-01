import pygame


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
            raise ValueError("Opacity factor must be greater than zero and lesser than 255.")
        self._opacity = new_opacity
        self._image.set_alpha(new_opacity)
