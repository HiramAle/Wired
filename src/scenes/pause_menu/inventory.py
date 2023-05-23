import pygame
from engine.assets import Assets
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, ItemSlot
from engine.inventory import Inventory as inventory


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
        Sprite((121 + self.x_padding, 251), Assets.images_book["cable_length"], self.inventory, centered=False)
        Sprite((205 + self.x_padding, 251), Assets.images_book["connectors"], self.inventory, centered=False)
        Text((143 + self.x_padding, 293.5), f"{inventory.items['cable']}m", 16, Colors.SPRITE, self.inventory)
        Text((227 + self.x_padding, 293.5), f"{inventory.items['connector']}p", 16, Colors.SPRITE,
             self.inventory)
        self.slots = []
        # for index, (quality, quantity) in enumerate(save_manager.active_save.inventory["cables"]["a"].items()):
        #     slot = ItemSlot((365 + (index * 64) + self.x_padding, 64), quality, "A", quantity, self.inventory)
        #     self.slots.append(slot)
        # for index, (quality, quantity) in enumerate(save_manager.active_save.inventory["cables"]["b"].items()):
        #     slot = ItemSlot((365 + (index * 64) + self.x_padding, 125), quality, "B", quantity, self.inventory)
        #     self.slots.append(slot)
        for index in range(3):
            slot = ItemSlot((365 + (index * 64) + self.x_padding, 64), str(index + 1), "Cruzado",
                            inventory.how_much(f"cable_crossover_{index + 1}"), self.inventory)
            self.slots.append(slot)
        for index in range(3):
            slot = ItemSlot((365 + (index * 64) + self.x_padding, 125), str(index + 1), "Directo",
                            inventory.how_much(f"cable_straight_{index + 1}"), self.inventory)
            self.slots.append(slot)
        self.item_name = Text((449 + self.x_padding, 251), "", 32, Colors.SPRITE, self.inventory)

    def update(self):
        self.inventory.update()
        for slot in self.slots:
            if slot.hovered:
                self.item_name.text = f"Cable {slot.standard}"

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.inventory.render(self.display)
