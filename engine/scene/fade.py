import pygame
from engine.time import Time
from engine.scene.scene import Scene
from engine.scene.transition import Transition
from src.constants.colors import DARK_BLACK_MOTION


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
            self.alpha += self.transitionSpeed * Time.dt
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
                self.fade_out = True
        if self.fade_out:
            self.toScene.update()
            self.alpha -= self.transitionSpeed * Time.dt
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_out = False

        if not self.fade_in and not self.fade_out:
            from engine.scene.scene_manager import SceneManager
            SceneManager.set_active_scene(self.toScene, swap=True)
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
