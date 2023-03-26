import pygame
import src.engine.time as time
import src.engine.window as window
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.game_object.game_object import GameObject
from src.entities.entity import Entity


class Camera(GameObject):
    def __init__(self):
        super().__init__("camera", (0, 0))
        self.entity_tracking: Entity | None = None
        self.target_position = pygame.math.Vector2((CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2))
        self.rate = 0.3
        self.timer = time.Timer(1)
        self.timer.start()

    def set_target(self, position: tuple):
        self.target_position = pygame.math.Vector2(position)

    def update(self):
        if self.entity_tracking:
            self.set_target((self.entity_tracking.x - CANVAS_WIDTH // 2, self.entity_tracking.y - CANVAS_HEIGHT // 2))

        self.position += (self.target_position - self.position) / (self.rate / time.dt)

        # if self.entity_tracking is not None:
        #     self.target_position = self.entity_tracking.rect.center
        #
        # diff = self.target_position - pygame.math.Vector2(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2) - self.position
        # if abs(diff.x) > 20:
        #     self.x += diff.x * time.dt
        # if abs(diff.y) > 20:
        #     self.y += diff.y * time.dt
