import pygame
from engine.assets import Assets
from engine.objects.sprite import Sprite
from engine.animation.animation import Animation
from engine.constants import Colors
from engine.ui.text import Text

categories = ["Inventario", "Trabajos", "Mapa", "Glosario", "Opciones", "Salir"]


class Category:
    def __init__(self, name: str):
        self.name = name
        self.page = pygame.Surface((640, 360), pygame.SRCALPHA)
        self.title = Text((185, 24), name, 32, Colors.SPRITE, shadow=False)

    def render(self, display: pygame.Surface):
        self.title.render(self.page)
        self.title.render(display)


class Tab(Sprite):
    def __init__(self, name: str, *groups):
        super().__init__((28 + 47, 30 + (27 * categories.index(name))), pygame.Surface((29, 20), pygame.SRCALPHA),
                         *groups)
        # Icon
        self.icon = Sprite((self.x - 10, self.rect.centery), Assets.images_book[name.lower()])
        # Animations
        self.tab_enter = Assets.animations["book"]["tab"]
        self.tab_enter.loop = False
        self.tab_exit = Assets.animations["book"]["tab"]
        self.tab_exit.reversed = True
        self.tab_exit.loop = False
        # self.tab_idle = self.tab_enter[-1]
        self.tab_selected = Assets.images_book["tab_selected"]
        self.tab_idle = Assets.images_book["tab_idle"]
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

    def update(self):
        if not self.animation.done:
            self.animation.update()
            self.image = self.animation.current_frame
            return
        # Animation ended
        if self.animation == self.tab_enter:
            self.entered = True
            self.entering = False
            self.image = self.tab_idle
        elif self.animation == self.tab_exit:
            self.exited = True
            self.image = pygame.Surface((29, 20), pygame.SRCALPHA)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        shadow = pygame.mask.from_surface(self.image.copy())
        shadow = shadow.to_surface(setcolor=Colors.BLACK, unsetcolor=(0, 0, 0))
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
        super().__init__((47, 20), Assets.images_book["book_background"], *groups)
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
        self.shadow = self.shadow.to_surface(setcolor=Colors.BLACK, unsetcolor=(0, 0, 0))
        self.shadow.set_colorkey((0, 0, 0))
        self.shadow.set_alpha(120)
        self.shadow_rect = self.rect
        self.shadow_rect.topleft = self.position
        self.shadow_rect.x += 2
        self.shadow_rect.y += 2
        self.bookmark = Sprite((103, 21),
                               Assets.images_book[f"bookmark_{self.current_category.name.lower()}"],
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
                self.bookmark.image = Assets.images_book[f"bookmark_{self.current_category.name.lower()}"]
                tab.selected = True

    def render(self, display: pygame.Surface, offset=(0, 0)):
        display.blit(self.shadow, self.shadow_rect)
        display.blit(self.image, self.position)
        self.current_category.render(display)
        self.bookmark.render(display)
        for index, tab in enumerate(self.tabs):
            tab.render(display)
