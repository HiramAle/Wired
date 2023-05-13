import pygame
import engine.assets as assets
from engine.objects.sprite import SpriteGroup
from src.constants.paths import *
from src.entities.actor import Actor
from engine.objects.sprite import Sprite
from src.components.animation import Animation
from src.utils.load import load_json
from src.utils.json_saver import instance as save_manager


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
        self.players_name = save_manager.game_save.name

        for index, dialog in enumerate(self.dialogs):
            dialog: str
            self.dialogs[index] = dialog.replace("@", self.players_name)

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
