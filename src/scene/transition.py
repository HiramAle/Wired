import math

import pygame
import src.scene.scene_manager as scene_manager
import src.engine.time as time
from src.constants.locals import CORNERS
from src.scene.scene import Scene
from src.constants.colors import *


class Transition(Scene):
    def __init__(self, name: str, to_scene: Scene, from_scene: Scene):
        super().__init__(name)
        self.fromScene: Scene = to_scene
        self.toScene: Scene = from_scene
        self.transitionSpeed = 300


class CircleTransition(Transition):
    def __init__(self, to_scene: Scene, from_scene: Scene):
        super().__init__("circle_transition", to_scene, from_scene)
        self.transitionSurface = from_scene.display.copy()
        self.transitionSurface.set_colorkey(WHITE_MOTION)
        self.circlePosition = self.fromScene.transitionPosition
        self.enterCircleRadius = self.get_max_circle_radius(self.circlePosition)
        self.exitCircleRadius = self.get_max_circle_radius(self.toScene.transitionPosition)
        self.circleRadius = self.enterCircleRadius
        self.transitioningIn = True
        pygame.mouse.set_visible(False)

    @staticmethod
    def get_max_circle_radius(point: tuple):
        value = max([math.dist(point, corner) for corner in CORNERS])
        return value

    def update(self):
        if self.transitioningIn:
            self.circleRadius -= time.dt * self.transitionSpeed
            if self.circleRadius <= 0:
                self.transitioningIn = False
                self.circlePosition = self.toScene.transitionPosition
        else:
            self.circleRadius += time.dt * self.transitionSpeed
            if self.circleRadius >= self.exitCircleRadius:
                scene_manager.set_scene(self.toScene, swap=True)
                pygame.mouse.set_visible(True)

    def render(self) -> None:
        if self.transitioningIn:
            self.fromScene.render()
            self.display.blit(self.fromScene.display, (0, 0))
        else:
            self.toScene.render()
            self.display.blit(self.toScene.display, (0, 0))
        self.transitionSurface.fill(DARK_BLACK_MOTION)
        pygame.draw.circle(self.transitionSurface, WHITE_MOTION, self.circlePosition, self.circleRadius)
        self.display.blit(self.transitionSurface, (0, 0))
