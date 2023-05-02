import pygame
import src.engine.time as time
import src.engine.input as input
import src.engine.data as data
import src.engine.assets as assets
from src.entities.entity import Entity
from src.game_object.sprite import SpriteGroup
import src.utils.load as load
from src.constants.paths import *
from src.entities.actor import Actor
from src.map.tiled_map import Trigger
from src.game_object.sprite import Sprite
from src.components.animation import Animation
import src.scene.core.scene_manager as scene_manager
from src.scene.cables.order import OrderCable
from src.scene.subnetting.subnetting import Subnetting
import src.scene.map.test_map as map_scene
from src.utils.load import load_json


class Emote(Sprite, Animation):
    def __init__(self, position: tuple, anim_data: list, *groups):
        Animation.__init__(self, anim_data)
        Sprite.__init__(self, "emote", position, self.frame, *groups)

    def update(self):
        self.play()
        self.image = self.frame


class NPC(Actor):
    def __init__(self, scene, name: str, position: tuple, collision: SpriteGroup, player, *groups, **kwargs):
        path = f"{NPC_SPRITE_SHEETS}/{name}.png"
        super().__init__(position, collision, path, *groups, **kwargs)
        self.name = "npc_" + name
        self.scene = scene
        self.active_trigger = None
        self.emote = Emote((self.rect.centerx, self.rect.top + 24), assets.animations["emotes"]["ask"])
        self.emote.loop = False
        self.emote_active = False
        self.player = player
        self.data = load_json(f"{NPC_DATA}/{name}.json")
        self.dialogs = self.data["dialogs"]
        self.talkable = False

    def check_player(self):
        if (self.player.position_vector - self.position_vector).magnitude() <= 60:
            self.emote_active = True
            self.talkable = True
        else:
            self.emote.rewind()
            self.emote_active = False
            self.talkable = False

    def update(self, *args, **kwargs):
        self.move()
        self.update_status()
        self.animate()
        self.emote.position = (self.rect.centerx, self.rect.top - 24)
        self.check_player()
        if self.emote_active:
            self.emote.update()

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display, offset)
        if self.emote_active:
            self.emote.render(display, offset)
