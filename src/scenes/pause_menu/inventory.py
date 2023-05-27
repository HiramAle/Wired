import pygame
from engine.assets import Assets
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, ItemSlot, SpecialItemSlot
from engine.inventory import Inventory as inventory
from engine.item_manager import ItemManager


class Inventory(Scene):
    def __init__(self):
        super().__init__("inventory")
        self.inventory = SpriteGroup()
        self.x_padding = 8
        Text((125 + self.x_padding, 38), "Inventario", 32, Colors.SPRITE, self.inventory, centered=False)
        Text((109 + self.x_padding, 74), save_manager.active_save.name, 32, Colors.SPRITE, self.inventory,
             centered=False)
        Text((241 + self.x_padding, 74), f"{inventory.money}G", 32, Colors.SPRITE, self.inventory,
             centered=False)
        Sprite((86 + self.x_padding, 80), Assets.images_book["character"], self.inventory, centered=False)
        Sprite((217 + self.x_padding, 80), Assets.images_book["money"], self.inventory, centered=False)
        self.avatar = PlayerAvatar((185 + 8, 173), "book", self.inventory)
        self.cable_slot = Sprite((121 + self.x_padding, 251), Assets.images_book["cable_length"], self.inventory,
                                 centered=False)
        self.connector_slot = Sprite((205 + self.x_padding, 251), Assets.images_book["connectors"], self.inventory,
                                     centered=False)
        Text((143 + self.x_padding, 293.5), f"{inventory.how_much('cable')}m", 16, Colors.SPRITE, self.inventory)
        Text((227 + self.x_padding, 293.5), f"{inventory.how_much('connector')}p", 16, Colors.SPRITE,
             self.inventory)
        Text((449 + self.x_padding, 52.5), "Cable Directo", 16, Colors.SPRITE, self.inventory, shadow=True,
             shadow_opacity=50, shado_color="#A3A7C2")
        Text((449 + self.x_padding, 115.5), "Cable Cruzado", 16, Colors.SPRITE, self.inventory, shadow=True,
             shadow_opacity=50, shado_color="#A3A7C2")
        Text((449 + self.x_padding, 175.5), "Objetos Especiales", 16, Colors.SPRITE, self.inventory, shadow=True,
             shadow_opacity=50, shado_color="#A3A7C2")
        self.slots = []
        for index in range(3):
            slot = ItemSlot((365 + (index * 64) + self.x_padding, 64),
                            ItemManager.get_item_by_id(f"cable_straight_{index + 1}"), self.inventory)
            self.slots.append(slot)
        for index in range(3):
            slot = ItemSlot((365 + (index * 64) + self.x_padding, 125),
                            ItemManager.get_item_by_id(f"cable_crossover_{index + 1}"), self.inventory)
            self.slots.append(slot)

        for index in range(3):
            SpecialItemSlot((365 + (index * 64) + self.x_padding, 186), "a", self.inventory)

        self.item_name = Text((449 + self.x_padding, 251 - 8), "", 32, Colors.SPRITE, self.inventory)
        self.item_description_frame = Sprite((344 + self.x_padding, 272 - 10), Assets.images_book["item_description"],
                                             self.inventory, centered=False)
        self.item_description = Text(self.item_description_frame.rect.center, "", 16, Colors.WHITE, self.inventory,
                                     max_width=210)

    def update(self):
        self.inventory.update()
        for slot in self.slots:
            if slot.hovered:
                self.item_name.text = slot.item.name
                self.item_description.text = slot.item.description
        if self.connector_slot.hovered:
            self.item_name.text = ItemManager.get_item_by_id("connector").name
            self.item_description.text = ItemManager.get_item_by_id("connector").description
        if self.cable_slot.hovered:
            self.item_name.text = ItemManager.get_item_by_id("cable").name
            self.item_description.text = ItemManager.get_item_by_id("cable").description

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.inventory.render(self.display)
