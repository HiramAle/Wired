import pygame
from engine.assets import Assets
from engine.input import Input
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.ui.text import Text
from engine.constants import Colors
from engine.playerdata import PlayerData
from engine.ui.button import Button
from engine.audio import AudioManager
from engine.window import Window


class Item:
    def __init__(self, name: str, icon: pygame.Surface, price: int):
        self.name = name
        self.icon = icon
        self.price = price


class ListItem(Sprite):
    def __init__(self, position: tuple, item: Item, *groups, **kwargs):
        super().__init__(position, Assets.images_store["item_element"], *groups, **kwargs)
        self.pivot = self.Pivot.TOP_LEFT
        self.item = item
        self.icon = Sprite((self.x + 18, self.y + 20), item.icon)
        self.name = Text((self.x + 41 + 8, self.y + 5), item.name, 32, Colors.SPRITE, centered=False)
        self.buy = Button((self.x + self.rect.width + 14, self.y + 2), Assets.images_store["buy_normal"],
                          Assets.images_store["buy_pressed"], centered=False)
        self.outline_width = 2
        self.outline_color = Colors.WHITE

    def is_hovered(self) -> bool:
        if self.hovered:
            return True
        if self.icon.hovered:
            return True
        if self.name.hovered:
            return True
        if self.buy.hovered:
            return True
        return False

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        rect = surface.get_rect(topleft=self.position)
        display.blit(surface, (rect.left + self.outline_width, rect.top))
        display.blit(surface, (rect.left - self.outline_width, rect.top))
        display.blit(surface, (rect.left, rect.top + self.outline_width))
        display.blit(surface, (rect.left, rect.top - self.outline_width))

    def update(self, *args, **kwargs):
        self.buy.update()

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.icon.render(display)
        self.name.render(display)
        self.buy.render(display)


class Store(Scene):
    def __init__(self):
        super().__init__("store")
        self.store_ui = SpriteGroup()
        Sprite((69, 52), Assets.images_store["background"], self.store_ui, centered=False)
        Sprite((14, 18), Assets.images_store["inventory_own"], self.store_ui, centered=False)
        self.cables = Text((68, 43), str(PlayerData.inventory.how_many("cable")), 32, Colors.SPRITE, self.store_ui)
        Sprite((20, 29), Assets.images_store["cable_icon"], self.store_ui, centered=False)
        Sprite((99, 18), Assets.images_store["inventory_own"], self.store_ui, centered=False)
        self.connectors = Text((150, 43), str(PlayerData.inventory.how_much("connector")), 32, Colors.SPRITE,
                               self.store_ui)
        Sprite((110, 27), Assets.images_store["connector_icon"], self.store_ui, centered=False)
        Sprite((477, 14), Assets.images_store["money"], self.store_ui, centered=False)
        self.money = Text((571, 43), f"{PlayerData.inventory.money}G", 32, Colors.SPRITE, self.store_ui)
        Sprite((104, 111), Assets.images_store["items_background"], self.store_ui, centered=False)
        Sprite((434, 111), Assets.images_store["icon_frame"], self.store_ui, centered=False)
        Sprite((434, 246), Assets.images_store["price_frame"], self.store_ui, centered=False)
        self.item_icon = Sprite((490, 176), pygame.Surface((32, 32), pygame.SRCALPHA), self.store_ui)
        self.item_price = Text((474, 273), "", 32, Colors.SPRITE, self.store_ui)
        self.items = [Item("Conector RJ45", Assets.images_store["connector_icon"], 5),
                      Item("Cable UTP CAT-6", Assets.images_store["cable_icon"], 10),
                      Item("Cable Serial", Assets.images_store["serial_icon"], 40)]
        self.list_items = []
        self.list_items.append(ListItem((112, 123), self.items[0], self.store_ui))
        self.list_items.append(ListItem((112, 165), self.items[1], self.store_ui))
        self.list_items.append(ListItem((112, 207), self.items[2], self.store_ui))
        self.ids = {0: "connectors", 1: "cables"}

    def update(self) -> None:
        self.store_ui.update()
        for index, item in enumerate(self.list_items):
            if item.is_hovered():
                self.item_icon.image = pygame.transform.scale_by(item.icon.image, 2)
                self.item_price.text = str(item.item.price)
            if item.buy.clicked:
                if PlayerData.inventory.money < item.item.price:
                    item.buy.state = item.buy.State.NORMAL
                    item.buy.sound_played = True
                    AudioManager.play_random_from("cancel")
                    break
                AudioManager.play_random_from("buy")
                PlayerData.inventory.money -= item.item.price
                self.money.text = f"{PlayerData.inventory.money}G"
                if index == 0:
                    PlayerData.add_item("connector", 1)
                    self.connectors.text = str(PlayerData.inventory.how_much("connector"))
                elif index == 1:
                    PlayerData.add_item("cable", 1)
                    self.cables.text = str(PlayerData.inventory.how_many("cable"))
                elif index == 2:
                    PlayerData.add_item("serial_cable", 1)

        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            SceneManager.exit_scene()

        # Change cursor
        if any([item.buy.hovered for item in self.list_items]):
            if Input.mouse.buttons["left_hold"]:
                Window.set_cursor("grab")
            else:
                Window.set_cursor("hand")
        else:
            Window.set_cursor("arrow")

    def render(self) -> None:
        self.store_ui.render(self.display)
