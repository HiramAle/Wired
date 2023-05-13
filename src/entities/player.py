import pygame
import engine.input as input
import engine.assets as assets
from engine.objects.sprite import SpriteGroup
from src.constants.paths import *
from src.entities.actor import Actor
from src.map.tiled_map import Trigger
from engine.objects.sprite import Sprite
from src.components.animation import Animation
from src.utils.json_saver import instance as save_manager


class Emote(Sprite, Animation):
    def __init__(self, position: tuple, anim_data: list, *groups):
        Animation.__init__(self, anim_data)
        Sprite.__init__(self, "emote", position, self.frame, *groups)

    def update(self):
        self.play()
        self.image = self.frame


class Player(Actor):
    def __init__(self, scene, position: tuple, collision: SpriteGroup, interactions: SpriteGroup,
                 *groups, **kwargs):
        path = f"{USER_DATA}/saves/save_{save_manager.index}/sprite_sheet.png"
        super().__init__(position, collision, path, *groups, **kwargs)
        self.interactions = interactions
        self.interact_icon = pygame.Surface((10, 10))
        self.interact_icon.fill("cyan")
        self.scene = scene
        self.active_trigger = None
        self.emote = Emote((self.rect.centerx, self.rect.top + 24), assets.animations["emotes"]["alert"])
        self.emote.loop = False
        self.emote_active = False

    def input(self):
        self.movement.x, self.movement.y = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x = - 1
        if keys[pygame.K_d]:
            self.movement.x = 1
        if keys[pygame.K_w]:
            self.movement.y = - 1
        if keys[pygame.K_s]:
            self.movement.y = 1

    def check_triggers(self):
        if not self.active_trigger:
            for trigger in self.interactions.sprites():
                trigger: Trigger
                if self.collider.colliderect(trigger.rect):
                    self.active_trigger = trigger
                    self.active_trigger.on_enter(player=self)
                    if self.active_trigger.name != "stairs":
                        self.emote_active = True
                    break
            if not self.active_trigger:
                self.emote_active = False
                self.emote.rewind()
                return
        if not self.collider.colliderect(self.active_trigger.rect):
            self.active_trigger.on_exit(player=self)
            self.active_trigger = None

    def update(self, *args, **kwargs):
        self.input()
        self.move()
        self.update_status()
        self.animate()
        self.check_triggers()
        self.emote.position = (self.rect.centerx, self.rect.top - 24)
        if self.emote_active:
            self.emote.update()

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display, offset)
        if self.active_trigger and input.keyboard.keys["interact"]:
            if "scenes" in self.active_trigger.name:
                self.scene.change_scene(self.active_trigger.name)
            if "sleep" in self.active_trigger.name:
                save_manager.game_save.time += pygame.time.get_ticks()
                save_manager.game_save.save()
        if self.emote_active:
            self.emote.render(display, offset)
