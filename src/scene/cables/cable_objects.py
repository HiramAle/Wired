import pygame
import src.engine.assets as assets
import src.engine.window as window
import src.engine.input as input
import src.engine.time as time
from src.game_object.sprite import Sprite
from src.components.animation import Animation
from src.constants.colors import DARK_BLACK_MOTION, WHITE_MOTION, GREEN_MOTION, RED_MOTION


class Cable(Sprite):
    def __init__(self, position: tuple, color: str, name: str, *groups, **kwargs):
        image = assets.images_cables[f"{name.split('_')[0].lower()}_{color.lower()}"]
        super().__init__(name, position, image, *groups, **kwargs)
        self.color = color
        self.scale = 2
        shadow_mask = pygame.mask.from_surface(self.image)
        self.shadow = shadow_mask.to_surface(setcolor=DARK_BLACK_MOTION, unsetcolor=(0, 0, 0))
        self.shadow.set_colorkey((0, 0, 0))
        self.shadow.set_alpha(60)
        self.shadowActive = True
        self.swapping = False
        self.new_position = 0
        self.dragging = False
        self.outline_color = WHITE_MOTION
        self.right_order = False
        self.colored_outline = False

    def update(self):
        if self.swapping:
            self.y -= (self.y - self.new_position) / (0.1 / time.dt)
            if abs(self.y - self.new_position) <= 0.5:
                self.y = self.new_position
                self.swapping = False

        if self.right_order:
            self.outline_color = GREEN_MOTION
        elif not self.dragging:
            self.outline_color = RED_MOTION

    def swap(self, position: int | float):
        self.new_position = position
        self.swapping = True

    def render(self, display: pygame.Surface, offset=(0, 0)):
        if self.dragging or self.colored_outline:
            if self.dragging:
                self.outline_color = WHITE_MOTION
            mask = pygame.mask.from_surface(self.image)
            mask_surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
            mask_surface.set_colorkey((0, 0, 0))
            display.blit(mask_surface, (self.rect.x - 2, self.rect.y))
            display.blit(mask_surface, (self.rect.x + 2, self.rect.y))
            display.blit(mask_surface, (self.rect.x, self.rect.y - 2))
            display.blit(mask_surface, (self.rect.x, self.rect.y + 2))
        else:
            display.blit(self.shadow, (self.rect.x + 1, self.rect.y + 2))
        super().render(display, offset)

    def __repr__(self):
        return str(self.name)


class CrimpTool(Sprite, Animation):
    def __init__(self, position: tuple, data: list, *groups, **kwargs):
        Animation.__init__(self, data)
        Sprite.__init__(self, "crimp_tool", position, self.frame, *groups, **kwargs)
        self.default_image = assets.images_cables["crimp_tool"]
        self.image = self.default_image
        self.set = False
        self.loop = False
        self.playing = False

    @property
    def crimp_area(self) -> pygame.Rect:
        return pygame.Rect(self.x - 130, self.rect.centery - 25, 50, 50)

    def update(self):
        if self.set:
            self.image = self.frame
            if self.playing:
                self.play()
        else:
            self.image = self.default_image

        # if self.set:
        #     self.image = self.frame
        #     if input.mouse.buttons["left"]:
        #         self.playing = True
        #     if self.playing:
        #         self.play()
        #         if self.done:
        #             self.playing = False
        #             self.rewind()
        #             self.image = self.default_image
        #
        # else:
        #     self.playing = False
        #     self.rewind()
        #     self.image = self.default_image
        ...
        # if self.moving:
        #     self.image = self.default_image
        # else:
        #     self.image = self.frame

        # Update collider
        # if self.playing:
        #     self.play()

        # if self.actual_frame >= len(self.frames) - 1:
        #     self.playing = False
