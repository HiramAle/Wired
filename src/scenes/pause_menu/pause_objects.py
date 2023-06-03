import pygame
from engine.objects.sprite import Sprite
from engine.assets import Assets
from engine.input import Input
from engine.ui.text import Text
from engine.constants import Colors
from enum import Enum
from src.scenes.world.player import Player
from engine.item import Item
from engine.playerdata import PlayerData


class Tab(Sprite):
    class State(Enum):
        IDLE = 0
        ENTERING = 1
        SELECTED = 2
        EXITING = 3
        HIDE = 4

    def __init__(self, position: tuple, name: str, *groups, **kwargs):
        super().__init__(position, pygame.Surface(Assets.images_book["tab_idle"].get_size(), pygame.SRCALPHA), *groups,
                         **kwargs)
        self.pivot = self.Pivot.TOP_LEFT
        self.name = name.lower()
        self.icon = Sprite((self.x + 20, self.rect.centery), Assets.images_book[name.lower()])
        # ---------- Animations ----------
        enter_animation = Assets.animations["book"]["tab"].copy()
        enter_animation.loop = False
        exit_animation = Assets.animations["book"]["tab"].copy()
        exit_animation.loop = False
        exit_animation.invert_order()
        self.animations = {self.State.ENTERING: enter_animation, self.State.EXITING: exit_animation}
        self._current_animation = self.animations[self.State.ENTERING]
        self.state = self.State.ENTERING

    def set_state(self, new_state: State):
        if new_state == self.state:
            return
        # print(f"changing state from {self.state} to {new_state}")
        self.state = new_state
        if new_state in self.animations.keys():
            self._current_animation = self.animations[new_state]
            self._current_animation.rewind()
            self._current_animation.play()
        elif new_state == self.State.IDLE:
            self.image = Assets.images_book["tab_idle"]
            self.icon.x = self.x + 20
        elif new_state == self.State.SELECTED:
            self.image = Assets.images_book["tab_selected"]
            self.icon.x = self.x + 15
        elif new_state == self.State.HIDE:
            self.image = pygame.Surface(Assets.images_book["tab_idle"].get_size(), pygame.SRCALPHA)

    def update(self, *args, **kwargs):
        if self.clicked:
            self.set_state(self.State.SELECTED)

        if self.state in [self.State.ENTERING, self.State.EXITING]:
            self._current_animation.update()
            self.image = self._current_animation.current_frame
            if self._current_animation.done:
                if self.state == self.State.ENTERING:
                    self.set_state(self.State.IDLE)
                if self.state == self.State.EXITING:
                    self.set_state(self.State.HIDE)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.icon.render(display)


class PlayerAvatar(Sprite):
    def __init__(self, position: tuple, action: str, *groups, **kwargs):
        super().__init__(position, pygame.Surface((64, 128), pygame.SRCALPHA), *groups, **kwargs)
        self.player = Player((0, 0), [], [], [])
        self.player.action = action

    def update(self, *args, **kwargs):
        self.image = pygame.Surface((64, 128), pygame.SRCALPHA)
        self.player.animate()
        self.image.blit(pygame.transform.scale_by(self.player.image, 2), (0, 0))


class ItemSlot(Sprite):
    def __init__(self, position: tuple, item: Item, *groups, **kwargs):
        super().__init__(position, Assets.images_book[f"cable_{item.id[-1]}"], *groups, **kwargs)
        self.item = item
        self.pivot = self.Pivot.TOP_LEFT
        self.quantity = Text((self.x + 31, self.y + 32.5), str(PlayerData.inventory.how_much(item.id)), 16,
                             Colors.WHITE)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.quantity.render(display)


class SpecialItemSlot(Sprite):
    def __init__(self, position: tuple, item: Item, *groups, **kwargs):
        if item.id == "serial_cable":
            image = Assets.images_book["item_multiple"]
        else:
            if PlayerData.inventory.has("usb_double_cable"):
                image = Assets.images_book["USB_item"]
            else:
                image = Assets.images_book["empty_item"]

        super().__init__(position, image, *groups)
        self.pivot = self.Pivot.TOP_LEFT
        self.item = item
        self.unique = kwargs.get("unique", True)
        self.quantity = Text((self.x + 31, self.y + 32.5), str(PlayerData.inventory.how_much(item.id)), 16,
                             Colors.WHITE)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        if not self.unique:
            self.quantity.render(display)


class Button(Sprite):
    class State(Enum):
        NORMAL = 0
        PRESSED = 1
        HOVERED = 2

    def __init__(self, position: tuple, name: str, *groups, **kwargs):
        super().__init__(position, Assets.images_book[f"{name}_normal"], *groups, **kwargs)
        self.name = name
        self.state = self.State.NORMAL
        self.outline_width = 2
        self.outline_color = Colors.WHITE

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
            self.image = Assets.images_book[f"{self.name}_pressed"]
        else:
            self.image = Assets.images_book[f"{self.name}_normal"]

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.hovered:
            self.draw_outline(display)
        super().render(display)


class Accessory(Sprite):
    def __init__(self):
        super().__init__((100, 100), pygame.Surface((64, 128), pygame.SRCALPHA))
