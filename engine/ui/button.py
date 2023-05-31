import pygame
from enum import Enum
from engine.ui.ui_element import UIElement
from engine.constants import Colors
from engine.input import Input


class Button(UIElement):
    class State(Enum):
        NORMAL = 0
        PRESSED = 1
        HOVERED = 2

    def __init__(self, position: tuple, normal_state: pygame.Surface, pressed_state: pygame.Surface, *groups, **kwargs):
        super().__init__(position, normal_state, *groups, **kwargs)
        self.state = self.State.NORMAL
        self.outline_width = 2
        self.outline_color = Colors.WHITE
        self.normal_image = normal_state
        self.pressed_image = pressed_state

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        if self.pivot == self.Pivot.CENTER:
            rect = surface.get_rect(center=self.position)
        elif self.pivot == self.Pivot.TOP_LEFT:
            rect = surface.get_rect(topleft=self.position)

        display.blit(surface, (rect.left + self.outline_width, rect.top))
        display.blit(surface, (rect.left - self.outline_width, rect.top))
        display.blit(surface, (rect.left, rect.top + self.outline_width))
        display.blit(surface, (rect.left, rect.top - self.outline_width))

    def update(self, *args, **kwargs):
        if self.hovered and Input.mouse.buttons["left_hold"]:
            self.image = self.pressed_image
        else:
            self.image = self.normal_image

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.hovered:
            self.draw_outline(display)
        super().render(display)
