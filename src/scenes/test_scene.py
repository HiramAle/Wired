import pygame
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.assets import Assets
from engine.input import Input
from engine.ui.text import Text
from engine.constants import Colors
from engine.loader import Loader
from enum import Enum
from engine.time import Timer, Time
from engine.animation.animation import Animation
from engine.save_manager import instance as save_manager
from engine.preferences import Preferences
from src.scenes.world.player import Player


class Tab(Sprite):
    class State(Enum):
        IDLE = 0
        ENTERING = 1
        SELECTED = 2
        EXITING = 3
        HIDE = 4

    def __init__(self, position: tuple, name: str):
        super().__init__(position, pygame.Surface(Assets.images_book["tab_idle"].get_size(), pygame.SRCALPHA))
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
        print(f"changing state from {self.state} to {new_state}")
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
        super().__init__(position, pygame.Surface((64, 96), pygame.SRCALPHA), *groups, **kwargs)
        self.player = Player((0, 0), [], [], [])
        self.player.action = action

    def update(self, *args, **kwargs):
        self.image = pygame.Surface((64, 96), pygame.SRCALPHA)
        self.player.animate()
        self.image.blit(pygame.transform.scale_by(self.player.image, 2), (0, 0))


class ItemSlot(Sprite):
    def __init__(self, position: tuple, quality: str, standard: str, quantity: int, *groups, **kwargs):
        super().__init__(position, Assets.images_book[f"cable_{quality}"], *groups, **kwargs)
        self.pivot = self.Pivot.TOP_LEFT
        self.standard = standard
        self.quality = Text((self.x + 11, self.y + 9.5), standard, 16, Colors.WHITE)
        self.quantity = Text((self.x + 31, self.y + 32.5), str(quantity), 16, Colors.WHITE)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.quality.render(display)
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


class TestScene(Scene):
    def __init__(self):
        super().__init__("test")
        # ---------- Book ----------
        self.categories = ["Inventario", "Trabajos", "Mapa", "Glosario", "Opciones", "Salir"]
        self.book_background = Sprite((39, 16), Assets.images_book["book_background"], centered=False)
        self.tabs = [Tab((39, 50 + (index * 30)), name) for index, name in enumerate(self.categories)]
        self.selected_tab = self.tabs[0]
        self.selected_tab.set_state(self.selected_tab.State.SELECTED)
        self.bookmark = Sprite((95, 17), Assets.images_book[f"bookmark_{self.selected_tab.name}"], centered=False)
        self.x_padding = 8
        # ---------- Inventory ----------
        self.inventory = SpriteGroup()
        Text((125 + self.x_padding, 38), "Inventario", 32, Colors.SPRITE, self.inventory, centered=False)
        Text((109 + self.x_padding, 74), save_manager.active_save.name, 32, Colors.SPRITE, self.inventory,
             centered=False)
        Text((241 + self.x_padding, 74), f"{save_manager.active_save.money}G", 32, Colors.SPRITE, self.inventory,
             centered=False)
        Sprite((86 + self.x_padding, 80), Assets.images_book["character"], self.inventory, centered=False)
        Sprite((217 + self.x_padding, 80), Assets.images_book["money"], self.inventory, centered=False)
        PlayerAvatar((185 + 8, 173), "book", self.inventory)
        Sprite((121 + self.x_padding, 251), Assets.images_book["cable_length"], self.inventory, centered=False)
        Sprite((205 + self.x_padding, 251), Assets.images_book["connectors"], self.inventory, centered=False)
        Text((143 + self.x_padding, 293.5), f"{save_manager.active_save.cable}m", 16, Colors.SPRITE, self.inventory)
        Text((227 + self.x_padding, 293.5), f"{save_manager.active_save.connectors}p", 16, Colors.SPRITE,
             self.inventory)
        self.slots = []
        for index, (quality, quantity) in enumerate(save_manager.active_save.inventory["cables"]["a"].items()):
            slot = ItemSlot((365 + (index * 64) + self.x_padding, 64), quality, "A", quantity, self.inventory)
            self.slots.append(slot)
        self.standard_b = []
        for index, (quality, quantity) in enumerate(save_manager.active_save.inventory["cables"]["b"].items()):
            slot = ItemSlot((365 + (index * 64) + self.x_padding, 125), quality, "B", quantity, self.inventory)
            self.slots.append(slot)
        self.item_name = Text((449 + self.x_padding, 251), "", 32, Colors.SPRITE, self.inventory)
        # ---------- Jobs ----------
        # ---------- Map ----------
        self.map = SpriteGroup()
        Sprite((4, 0), Assets.images_book["map"], self.map, centered=False)
        # ---------- Glossary ----------
        # ---------- Options ----------
        self.options = SpriteGroup()
        Text((140 + self.x_padding, 42), "Opciones", 32, Colors.SPRITE, self.options, centered=False)
        Text((128 + self.x_padding, 105), "Resolución", 32, Colors.SPRITE, self.options, centered=False)
        self.resolution = Text((188 + self.x_padding, 152), f"{Preferences.window_width} x {Preferences.window_height}",
                               32, Colors.SPRITE, self.options)
        Text((146 + self.x_padding, 199), "Volúmen", 32, Colors.SPRITE, self.options, centered=False)
        self.volume = Text((188 + self.x_padding, 241), f"{int(Preferences.volume * 100 / 20)}%",
                           32, Colors.SPRITE, self.options)
        Text((403 + self.x_padding, 42), "Controles", 32, Colors.SPRITE, self.options, centered=False)
        Text((470 + self.x_padding, 105), "Moverse", 16, Colors.SPRITE, self.options, centered=False)
        Text((497 + self.x_padding, 171), "Arrastrar", 16, Colors.SPRITE, self.options, centered=False)
        Text((373 + self.x_padding, 171), "Interactuar", 16, Colors.SPRITE, self.options, centered=False)
        Text((388 + self.x_padding, 226), "Inventario", 16, Colors.SPRITE, self.options, centered=False)
        Text((505 + self.x_padding, 226), "Opciones", 16, Colors.SPRITE, self.options, centered=False)
        Text((377 + self.x_padding, 258), "Glosario", 16, Colors.SPRITE, self.options, centered=False)
        Text((505 + self.x_padding, 258), "Salir", 16, Colors.SPRITE, self.options, centered=False)
        Sprite((407 + self.x_padding, 88), Assets.images_book["key_w"], self.options, centered=False)
        Sprite((383 + self.x_padding, 115), Assets.images_book["key_a"], self.options, centered=False)
        Sprite((407 + self.x_padding, 115), Assets.images_book["key_s"], self.options, centered=False)
        Sprite((431 + self.x_padding, 115), Assets.images_book["key_d"], self.options, centered=False)
        Sprite((345 + self.x_padding, 167), Assets.images_book["key_e"], self.options, centered=False)
        Sprite((466 + self.x_padding, 166), Assets.images_book["key_mouse"], self.options, centered=False)
        Sprite((345 + self.x_padding, 219), Assets.images_book["key_tab"], self.options, centered=False)
        Sprite((466 + self.x_padding, 219), Assets.images_book["key_o"], self.options, centered=False)
        Sprite((345 + self.x_padding, 253), Assets.images_book["key_g"], self.options, centered=False)
        Sprite((466 + self.x_padding, 253), Assets.images_book["key_esc"], self.options, centered=False)
        # ---------- Exit ----------
        self.exit = SpriteGroup()
        Text((155 + self.x_padding, 42), "Salir", 32, Colors.SPRITE, self.exit, centered=False)
        Text((455.5 + self.x_padding, 76.5 - 20), "Zzzz.", 16, Colors.SPRITE, self.exit)
        Text((455.5 + self.x_padding, 76.5 + 20), "Duerme para guardar tu progreso.", 16, Colors.SPRITE, self.exit)
        Text((456 + self.x_padding, 127),
             "La próxima vez\nque entres,\nretomaras desde\nel ultimo día\nen que hayas\ndormido. ", 16, Colors.SPRITE,
             self.exit, centered=False)
        Sprite((390.5 + self.x_padding, 208), Assets.images_book["bed"],self.exit)
        PlayerAvatar((390.5 + self.x_padding, 208), "sleep", self.exit)
        self.menu_button = Button((104, 120), "button_menu", self.exit, centered=False)
        self.desktop_button = Button((104, 194), "button_desktop", self.exit, centered=False)
        self.module_button = Button((104, 268), "button_module", self.exit, centered=False)
        # ---------- Other ----------
        self.category: SpriteGroup = self.inventory

    def update(self) -> None:
        self.category.update()
        for tab in self.tabs:
            tab.update()
            if tab.clicked and tab != self.selected_tab:
                self.bookmark.image = Assets.images_book[f"bookmark_{tab.name}"]
                self.selected_tab.set_state(self.selected_tab.State.IDLE)
                self.selected_tab = tab
                self.selected_tab.set_state(self.selected_tab.State.SELECTED)
                if tab.name == "mapa":
                    self.category = self.map
                elif tab.name == "inventario":
                    self.category = self.inventory
                elif tab.name == "opciones":
                    self.category = self.options
                elif tab.name == "salir":
                    self.category = self.exit
        if self.category == self.inventory:
            for slot in self.slots:
                if slot.hovered:
                    self.item_name.text = f"Cable T568{slot.standard}"
        if self.category == self.exit:
            from engine.scene.scene_manager import SceneManager
            if self.menu_button.clicked:
                from src.scenes.main_menu.main_menu import MainMenu
                SceneManager.change_scene(MainMenu(), True)
            if self.desktop_button.clicked:
                import sys
                sys.exit()
        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            SceneManager.exit_scene()

    def render(self) -> None:
        from engine.scene.scene_manager import SceneManager
        self.display.blit(SceneManager.stack_scene[-2].display, (0, 0))
        self.book_background.render(self.display)
        self.bookmark.render(self.display)
        for tab in self.tabs:
            tab.render(self.display)

        self.category.render(self.display)
        # pygame.draw.line(self.display, Colors.RED, (320, 0), (320, 360))
        # pygame.draw.line(self.display, Colors.GREEN, (self.book_background.rect.centerx, 0),
        #                  (self.book_background.rect.centerx, 360))
