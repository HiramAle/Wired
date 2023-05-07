import pygame
import src.engine.time as game_time
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.scene.world.actor import Actor
from src.scene.world.game_object import GameObject


class Camera(GameObject):
    def __init__(self, map_width: float, map_height: float, position=(0, 0)):
        super().__init__(position)
        self._target = self._position.copy()
        self._rate = 0.2
        self._actor: None | Actor = None
        self.map_width = map_width
        self.map_height = map_height
        self.offset = pygame.Vector2()

    @property
    def actor_tracking(self) -> None | Actor:
        return self._actor

    @actor_tracking.setter
    def actor_tracking(self, value: Actor):
        self._actor = value

    @property
    def target_position(self) -> tuple:
        return self._target.x, self._target.y

    @target_position.setter
    def target_position(self, value: tuple):
        self._target.x, self._target.y = value

    def update(self):
        if self._actor:
            distance_x = self._actor.x - CANVAS_WIDTH / 2
            distance_y = self._actor.y - CANVAS_HEIGHT / 2
            self.target_position = distance_x, distance_y

        if (self._target - self._position).magnitude() > 1:
            self._position += (self._target - self._position) / (self._rate / game_time.dt)

        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        if self.x > self.map_width - CANVAS_WIDTH:
            self.x = self.map_width - CANVAS_WIDTH

        if self.y > self.map_height - CANVAS_HEIGHT:
            self.y = self.map_height - CANVAS_HEIGHT

        self.offset.x = int(self.x)
        self.offset.y = int(self.y)
