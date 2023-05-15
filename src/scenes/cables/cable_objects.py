import pygame
from engine.assets import Assets
from engine.time import Time
from engine.objects.sprite import Sprite
from engine.constants import Colors


class Cable(Sprite):
    def __init__(self, position: tuple, color: str, name: str, *groups, **kwargs):
        image = Assets.images_cables[f"{name.split('_')[0].lower()}_{color.lower()}"]
        super().__init__(position, image, *groups, **kwargs)
        self.name = name
        self.color = color
        self.scale = 2
        shadow_mask = pygame.mask.from_surface(self.image)
        self.shadow = shadow_mask.to_surface(setcolor=Colors.DARK, unsetcolor=(0, 0, 0))
        self.shadow.set_colorkey((0, 0, 0))
        self.shadow.set_alpha(60)
        self.shadowActive = True
        self.swapping = False
        self.new_position = 0
        self.dragging = False
        self.outline_color = Colors.WHITE
        self.right_order = False
        self.colored_outline = False

    def update(self):
        if self.swapping:
            self.y -= (self.y - self.new_position) / (0.1 / Time.dt)
            if abs(self.y - self.new_position) <= 0.5:
                self.y = self.new_position
                self.swapping = False

        if self.right_order:
            self.outline_color = Colors.GREEN
        elif not self.dragging:
            self.outline_color = Colors.RED

    def swap(self, position: int | float):
        self.new_position = position
        self.swapping = True

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.dragging or self.colored_outline:
            if self.dragging:
                self.outline_color = Colors.WHITE
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


class CrimpTool(Sprite):
    def __init__(self, position: tuple, *groups, **kwargs):
        super().__init__(position, Assets.animations["cables"]["crimp"].current_frame, *groups, **kwargs)
        self.animation = Assets.animations["cables"]["crimp"]
        self.animation.loop = False
        self.default_image = Assets.images_cables["crimp_tool"]
        self.image = self.default_image
        self.set = False
        self.loop = False
        self.playing = False

    @property
    def crimp_area(self) -> pygame.Rect:
        return pygame.Rect(self.x - 130, self.rect.centery - 25, 50, 50)

    def move(self, position: tuple):
        self.x -= (self.x - position[0]) / (0.1 / Time.dt)
        self.y -= (self.y - position[1]) / (0.1 / Time.dt)

    def update(self):
        if self.set:
            self.image = self.animation.current_frame
            if self.playing:
                self.animation.update()
                self.image = self.animation.current_frame
        else:
            self.image = self.default_image
