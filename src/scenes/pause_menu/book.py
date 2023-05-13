import pygame
import engine.assets as game_assets
from engine.objects.sprite import Sprite
from src.components.animation import Animation
from src.constants.colors import *
from src.gui.text import GUIText

categories = ["Inventario", "Trabajos", "Mapa", "Glosario", "Opciones", "Salir"]


class Page:
    def __init__(self, side: str):
        self.position = (29 + 47, 20) if side == "left" else (290 + 47, 0)
        self.canvas = pygame.Surface((256, 320), pygame.SRCALPHA)
        self.x = self.position[0]
        self.y = self.position[1]
        self.center_x = self.canvas.get_width() / 2
        self.center_y = self.canvas.get_height() / 2
        self.true_center_x = self.x + self.center_x
        self.true_center_y = self.y + self.center_y

    def update(self):
        ...

    def render(self, display: pygame.Surface):
        display.blit(self.canvas, self.position)


class Category:
    def __init__(self, name: str):
        self.name = name
        self.left_page = Page("left")
        self.right_page = Page("right")
        mid_canvas = self.left_page.canvas.get_rect().centerx
        self.title = GUIText(name, (mid_canvas, 24), 32, color=BLACK_SPRITE, shadow=False)

    def render(self, display: pygame.Surface):
        self.title.render(self.left_page.canvas)
        self.left_page.render(display)
        self.right_page.render(display)


class Tab(Sprite):
    def __init__(self, name: str, *groups):
        super().__init__(name, (28 + 47, 30 + (27 * categories.index(name))), pygame.Surface((29, 20), pygame.SRCALPHA),
                         *groups)
        # Icon
        self.icon = Sprite("icon", (self.x - 10, self.rect.centery), game_assets.images_book[name.lower()])
        # Animations
        animation_data = game_assets.animations["book"]["tab"]
        self.tab_enter = Animation(animation_data)
        self.tab_enter.loop = False
        self.tab_exit = Animation([list(reversed(animation_data[0])), animation_data[1]])
        self.tab_exit.loop = False
        # self.tab_idle = self.tab_enter[-1]
        self.tab_selected = game_assets.images_book["tab_selected"]
        self.tab_idle = game_assets.images_book["tab_idle"]
        self.entered = False
        self.exited = False
        self._selected = False
        self.animation = self.tab_enter
        self.entering = True
        self.leaving = False

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(topright=self.position)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        if value == self._selected:
            return
        if value:
            self.image = self.tab_selected
        else:
            self.image = self.tab_idle
        self._selected = value

    def play(self):
        if not self.animation.done:
            self.animation.play()
            self.image = self.animation.frame
            return
        # Animation ended
        if self.animation == self.tab_enter:
            self.entered = True
            self.entering = False
            self.image = self.tab_idle
        elif self.animation == self.tab_exit:
            self.exited = True
            self.image = pygame.Surface((29, 20), pygame.SRCALPHA)

    def render(self, display: pygame.Surface, offset=(0, 0)):
        shadow = pygame.mask.from_surface(self.image.copy())
        shadow = shadow.to_surface(setcolor=BLACK_MOTION, unsetcolor=(0, 0, 0))
        shadow.set_colorkey((0, 0, 0))
        shadow_rect = self.rect
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow.set_alpha(120)
        display.blit(shadow, shadow_rect)
        super().render(display, offset)
        if self.entered and not self.entering and not self.leaving:
            if self.image == self.tab_idle:
                self.icon.x = self.x - 10
            if self.image == self.tab_selected:
                self.icon.x = self.x - 15
            self.icon.render(display)


class Book(Sprite):
    def __init__(self, index: int, categories_objects: list[Category], *groups):
        super().__init__("book", (47, 20), game_assets.images_book["book_background"], *groups)
        # Categories and tabs
        self._index = index
        self.categories = categories_objects
        self.tabs: list[Tab] = [Tab(category) for category in categories]
        self.loading_tab_index = 0
        self.loading = True
        self.exiting = False
        self.close = False
        self.current_category = self.categories[index]
        self.selected_tab = self.tabs[index]
        # Shadow
        self.shadow = pygame.mask.from_surface(self.image.copy())
        self.shadow = self.shadow.to_surface(setcolor=BLACK_MOTION, unsetcolor=(0, 0, 0))
        self.shadow.set_colorkey((0, 0, 0))
        self.shadow.set_alpha(120)
        self.shadow_rect = self.rect
        self.shadow_rect.topleft = self.position
        self.shadow_rect.x += 2
        self.shadow_rect.y += 2
        self.bookmark = Sprite("bookmark", (103, 21),
                               game_assets.images_book[f"bookmark_{self.current_category.name.lower()}"],
                               centered=False)

    @property
    def loading_tab(self) -> Tab:
        return self.tabs[self.loading_tab_index]

    def update(self):
        if self.loading:
            self.loading_tab.play()
            if self.loading_tab.entered:
                self.loading_tab.animation = self.loading_tab.tab_exit
                if self.loading_tab == self.tabs[-1]:
                    self.loading = False
                    return
                if self.loading_tab.name == self.current_category.name:
                    self.loading_tab.selected = True
                self.loading_tab_index += 1
        if self.exiting:
            self.loading_tab.leaving = True
            self.loading_tab.play()
            if self.loading_tab.exited:
                if self.loading_tab == self.tabs[0]:
                    self.exiting = False
                    self.close = True
                    return
                self.loading_tab_index -= 1

        for index, tab in enumerate(self.tabs):
            if tab.clicked:
                self.selected_tab.selected = False
                self.selected_tab = tab
                self.current_category = self.categories[index]
                self.bookmark.image = game_assets.images_book[f"bookmark_{self.current_category.name.lower()}"]
                tab.selected = True

    def render(self, display: pygame.Surface, offset=(0, 0)):
        display.blit(self.shadow, self.shadow_rect)
        display.blit(self.image, self.position)
        self.current_category.render(display)
        self.bookmark.render(display)
        for index, tab in enumerate(self.tabs):
            tab.render(display)
