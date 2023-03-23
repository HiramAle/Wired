import pygame
import src.engine.assets as assets
import src.engine.window as window
from src.game_object.sprite import Sprite
from src.game_object.components import Animation
from src.constants.colors import DARK_BLACK_MOTION


class Cable(Sprite):
    def __init__(self, position: tuple, color: str, name: str, *groups, **kwargs):
        image = assets.images_cables[f"{name.split('_')[0].lower()}_{color.lower()}"]
        super().__init__(name, position, image, *groups, **kwargs)
        self.color = color
        self.scale = 2
        self.shadow = self.image.copy()
        self.shadow.set_colorkey(color)
        # self.shadow.fill(DARK_BLACK_MOTION)
        pygame.draw.rect(self.shadow, DARK_BLACK_MOTION, pygame.Rect(0, 0, 168, 16), border_radius=3)
        self.shadow.set_alpha(100)
        self.shadowActive = True

    def render(self, display: pygame.Surface):
        if self.shadowActive:
            shadow_rect = self.rect
            shadow_rect.y = self.rect.y + 2
            shadow_rect.x = self.rect.x - 2
            display.blit(self.shadow, shadow_rect)
        super().render(display)

    def __repr__(self):
        return str(self.name)


class CrimpTool(Sprite, Animation):
    def __init__(self, position: tuple, data: list, *groups, **kwargs):
        Animation.__init__(self, data)
        Sprite.__init__(self, "crimp_tool", position, self.frame, *groups, **kwargs)
        self.moving = True
        self.default_image = assets.images_cables["crimp_tool"]
        self.playing = False

        self.collider = pygame.Rect(self.x - 130, self.rect.centery - 25, 50, 50)

    def on_mouse_enter(self):
        window.set_cursor("hand")

    def on_mouse_exit(self):
        window.set_cursor("arrow")

    def rewind(self):
        self.actual_frame = 0
        self.playing = True

    def re_position(self, rect: pygame.Rect):
        self.x = 130 - 25 + rect.centerx
        self.y = rect.centery

    def update(self):
        hovered = self.hovered
        if self.moving:
            self.image = self.default_image
        else:
            self.image = self.frame

        # Update collider
        self.collider = pygame.Rect(self.x - 130, self.rect.centery - 25, 50, 50)

        if self.playing:
            self.play()

        if self.actual_frame >= len(self.frames) - 1:
            self.playing = False





