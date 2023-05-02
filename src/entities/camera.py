import pygame
import src.engine.time as time
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.game_object.game_object import GameObject
from src.entities.entity import Entity
from typing import Optional


class Camera(GameObject):
    """
    A class representing the camera used to track an Entity or a specific position.
    """

    def __init__(self, max_x, max_y):
        """
        Initializes a new Camera object.
        """
        super().__init__("camera", (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2))
        self._entity: Optional[Entity] = None
        self._target = pygame.math.Vector2(self.position)
        self._rate = 0.3
        self.max_x = max_x
        self.max_y = max_y

    @property
    def tracked_entity(self) -> Entity:
        return self._entity

    @tracked_entity.setter
    def tracked_entity(self, value: Entity):
        self._entity = value
        # self.position = value.position

    @property
    def target_position(self) -> tuple:
        return self._target.x, self._target.y

    @target_position.setter
    def target_position(self, value: tuple):
        self._target.x, self._target.y = value

    @property
    def speed(self) -> float:
        return self._rate * 10

    @speed.setter
    def speed(self, value: int | float):
        if value < 0:
            raise ValueError("Speed only can be positive.")
        self._rate = value / 10

    def update(self, *args, **kwargs):
        """
        Update the position of the camera.
        """
        if self._entity:
            distance_x = self._entity.x - CANVAS_WIDTH / 2
            distance_y = self._entity.y - CANVAS_HEIGHT / 2
            self.target_position = distance_x, distance_y

        if self.position != self.target_position:
            self.position += (self._target - self.position_vector) / (self._rate / time.dt)

        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        if self.x > self.max_x - 640:
            self.x = self.max_x - 640

        if self.y > self.max_y - 360:
            self.y = self.max_y - 360
