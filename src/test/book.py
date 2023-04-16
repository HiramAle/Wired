import os
import time
import pygame
import sys
import random

pygame.init()

categories = ["profile", "inventory", "equipment", "tasks", "save", "settings"]

window = pygame.display.set_mode((1280, 720))
canvas = pygame.Surface((640, 320))
clock = pygame.time.Clock()
dt = 0.2
mouse_x, mouse_y = 0, 0
left_click = False


class Page:
    def __init__(self, side: str):
        self.position = (29 + 47, 0) if side == "left" else (290 + 47, 0)
        self.canvas = pygame.Surface((256, 320), pygame.SRCALPHA)

    def update(self):
        ...

    def render(self, display: pygame.Surface):
        display.blit(self.canvas, self.position)


class Category:
    def __init__(self, name: str):
        self.name = name
        self.left_page = Page("left")
        self.right_page = Page("right")
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # self.left_page.canvas.fill(self.color)
        # self.right_page.canvas.fill(self.color)


class Tab:
    def __init__(self, name: str):
        self.name = name
        self.position = (28 + 47, 30 + (27 * categories.index(name)))
        self.tab_enter = [pygame.image.load(f"tab_enter/{frame}").convert_alpha() for frame in os.listdir("tab_enter")]
        self.tab_exit = list(reversed(
            [pygame.image.load(f"tab_enter/{frame}").convert_alpha() for frame in os.listdir("tab_enter")]))
        self.tab_idle = self.tab_enter[-1]
        self.tab_selected = pygame.image.load("tab_selected.png").convert_alpha()
        self.image = pygame.Surface((29, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topright=self.position)
        self.entered = False
        self.exited = False
        self.frame_index = 0
        self.animation_speed = 20
        self._selected = False

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

    @property
    def clicked(self) -> bool:
        if left_click and self.rect.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def enter(self):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.tab_enter):
            self.frame_index = len(self.tab_enter) - 1
            self.entered = True
            self.image = self.tab_idle
            self.frame_index = 0
        else:
            self.image = self.tab_enter[int(self.frame_index)]

    def exit(self):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.tab_exit):
            self.frame_index = len(self.tab_exit) - 1
            self.exited = True
            self.image = pygame.Surface((29, 20), pygame.SRCALPHA)
            self.frame_index = 0
        else:
            self.image = self.tab_exit[int(self.frame_index)]

    def update(self):
        ...

    def render(self, display: pygame.Surface):
        display.blit(self.image, self.rect)


class Book:
    def __init__(self, index: int):
        self.initial_tab = categories[index]
        self.position = (47, 0)
        self.categories: dict[str, Category] = {category: Category(category) for category in categories}
        self.actual_category: Category = self.categories[list(self.categories.keys())[index]]
        self.tabs: dict[str, Tab] = {category: Tab(category) for category in categories}
        self.loading_tab_index = 0
        self.loading_tab = self.tabs[list(self.tabs.keys())[self.loading_tab_index]]
        self.background = pygame.image.load("book_background.png").convert_alpha()
        self.loading = True
        self.exiting = False
        self.starting_time = 0
        self.elapsed_time = 0
        self.close = False

    def enter(self):
        if self.starting_time == 0:
            self.starting_time = time.time()

        for name, tab in self.tabs.items():
            if tab != self.loading_tab:
                continue

            tab.enter()
            if tab.entered and self.loading_tab_index < len(self.tabs) - 1:
                self.loading_tab_index += 1
                self.loading_tab = self.tabs[list(self.tabs.keys())[self.loading_tab_index]]
                if self.initial_tab == tab.name:
                    tab.selected = True
            elif tab.entered and self.loading_tab_index >= len(self.tabs) - 1:
                self.loading_tab_index = len(self.tabs) - 1
                self.loading = False
                if self.initial_tab == tab.name:
                    tab.selected = True
                self.elapsed_time = time.time() - self.starting_time
                print(f"tiempo pasao: {self.elapsed_time}")
                self.starting_time = 0
                self.elapsed_time = 0

    def exit(self):
        if self.starting_time == 0:
            self.starting_time = time.time()
        for name, tab in reversed(self.tabs.items()):
            if tab != self.loading_tab:
                continue
            tab.exit()
            if tab.exited and self.loading_tab_index > 0:
                self.loading_tab_index -= 1
                self.loading_tab = self.tabs[list(self.tabs.keys())[self.loading_tab_index]]
            elif tab.exited and self.loading_tab_index == 0:
                self.loading_tab_index = 0
                self.exiting = False
                self.elapsed_time = time.time() - self.starting_time
                print(f"tiempo pasao: {self.elapsed_time}")
                self.starting_time = 0
                self.elapsed_time = 0
                self.close = True

    def update(self):
        self.actual_category.left_page.update()
        self.actual_category.right_page.update()

        if self.loading:
            self.enter()

        if self.exiting:
            self.exit()

        for name, tab in self.tabs.items():
            tab.update()

            if tab.clicked:
                self.tabs[self.actual_category.name].selected = False
                self.actual_category = self.categories.get(name, None)
                tab.selected = True

    def render(self, display: pygame.Surface):
        display.blit(self.background, self.position)

        self.actual_category.left_page.render(display)
        self.actual_category.right_page.render(display)

        for tab in self.tabs.values():
            tab.render(display)


book: Book | None = None

while True:
    left_click = False
    for event in pygame.event.get():
        event: pygame.Event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if not book:
                    book = Book(5)
                elif not book.loading:
                    book.exiting = True

            if pygame.key.get_pressed()[pygame.K_TAB]:
                if not book:
                    book = Book(1)

    canvas.fill("#2e2e2e")

    mouse_x = int(pygame.mouse.get_pos()[0] / 1280 * 640)
    mouse_y = int(pygame.mouse.get_pos()[1] / 720 * 320)

    if book:
        book.update()
        book.render(canvas)
        if book.close:
            book = None

    window.blit(pygame.transform.scale(canvas, (1280, 720)), (0, 0))
    pygame.display.update()
    dt = clock.tick() / 1000
