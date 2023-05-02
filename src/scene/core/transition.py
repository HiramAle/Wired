import math

import pygame
import src.scene.core.scene_manager as scene_manager
import src.engine.time as game_time
from src.constants.locals import CORNERS
from src.scene.core.scene import Scene
from src.constants.colors import *


class Transition(Scene):
    """
    Base class for creating transitions between Scenes.
    """

    def __init__(self, name: str, to_scene: Scene, from_scene: Scene):
        """
        Initializes a new Transition object.
        :param name: The name of the transition.
        :param to_scene: The scene that the transition is transitioning to.
        :param from_scene: The scene that the transition is transitioning from.
        """
        super().__init__(name)
        self.fromScene: Scene = to_scene
        self.toScene: Scene = from_scene
        self.transitionSpeed = 700


class FadeTransition(Transition):
    def __init__(self, to_scene: Scene, from_scene: Scene):
        super().__init__("fade", to_scene, from_scene)
        self.transitionSpeed = 500
        self.alpha = 0
        self.fade_in = True
        self.fade_out = False
        self.fade_surface = pygame.Surface(to_scene.display.get_size(), pygame.SRCALPHA)

    def update(self) -> None:
        if self.fade_in:
            self.fromScene.update()
            self.alpha += self.transitionSpeed * game_time.dt
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
                self.fade_out = True
        if self.fade_out:
            self.toScene.update()
            self.alpha -= self.transitionSpeed * game_time.dt
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_out = False

        if not self.fade_in and not self.fade_out:
            scene_manager.set_scene(self.toScene, swap=True)
            pygame.mouse.set_visible(True)

    def render(self) -> None:
        if self.fade_in:
            self.fromScene.render()
            self.display.blit(self.fromScene.display, (0, 0))
        if self.fade_out:
            self.toScene.render()
            self.display.blit(self.toScene.display, (0, 0))
        self.fade_surface.fill(DARK_BLACK_MOTION)
        self.fade_surface.set_alpha(self.alpha)
        self.display.blit(self.fade_surface, (0, 0))


class CircularTransition(Transition):
    """
    Subclass of Transition that provides a circular transition effect.
    """

    def __init__(self, to_scene: Scene, from_scene: Scene):
        """
        Initializes a new CircularTransition object.
        :param to_scene: The scene that the transition is transitioning to.
        :param from_scene: The scene that the transition is transitioning from.
        """
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
    def get_max_circle_radius(point: tuple) -> float:
        """
        Calculate the maximum distance from a point to any of the corners of the screen.
        :param point: The point to calculate the distance from.
        :return: The maximum distance from the point to any of the corners of the screen.
        """
        return max([math.dist(point, corner) for corner in CORNERS])

    def update(self):
        """
        Update the circle radius and transition to the next scene if necessary.
        """
        if self.transitioningIn:
            self.circleRadius -= game_time.dt * self.transitionSpeed
            if self.circleRadius <= 0:
                self.transitioningIn = False
                self.circlePosition = self.toScene.transitionPosition

        else:
            self.circleRadius += game_time.dt * self.transitionSpeed
            if self.circleRadius >= self.exitCircleRadius:
                scene_manager.set_scene(self.toScene, swap=True)
                pygame.mouse.set_visible(True)

    def render(self) -> None:
        """
        Render the current state of the transition effect.
        """
        if self.transitioningIn:
            # self.fromScene.render()
            self.display.blit(self.fromScene.display, (0, 0))
        else:
            # self.toScene.render()
            self.display.blit(self.toScene.display, (0, 0))
        self.transitionSurface.fill(DARK_BLACK_MOTION)
        pygame.draw.circle(self.transitionSurface, WHITE_MOTION, self.circlePosition, self.circleRadius)
        self.display.blit(self.transitionSurface, (0, 0))
