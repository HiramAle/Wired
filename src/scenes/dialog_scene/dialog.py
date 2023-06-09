import pygame
from engine.objects.sprite import Sprite
from src.scenes.world.npc import NPC
from engine.assets import Assets
from engine.ui.text import Text
from engine.constants import Colors
from engine.input import Input
from engine.time import Time, Timer
from engine.playerdata import PlayerData
from engine.audio import AudioManager


class Dialog:
    def __init__(self, sentences: list[str]):
        self.sentences = sentences
        self.sentence_index = 0

    @property
    def end_dialog(self) -> bool:
        return self.sentence_index >= len(self.sentences) - 1

    @property
    def current_sentence(self) -> str:
        vocal_pronoun = {"el": "o", "ella": "a", "elle": "e"}
        possessive_pronoun = {"el": "el", "ella": "la", "elle": "le"}
        sentence = self.sentences[self.sentence_index].replace("name", PlayerData.name)
        sentence = sentence.replace("@", vocal_pronoun[PlayerData.pronoun])
        sentence = sentence.replace("*", possessive_pronoun[PlayerData.pronoun])
        return sentence

    def next_sentence(self):
        self.sentence_index += 1


class DialogBox(Sprite):
    def __init__(self, npc: NPC, text: list[str]):
        super().__init__((123, 246), Assets.images_world["dialog_box"])
        self.pivot = self.Pivot.TOP_LEFT
        self.dialogs = [Dialog(text)]
        self.dialog_index = 0
        self.npc = npc
        self.actor_name = Text((174.5, 336), npc.data["name"], 32, Colors.SPRITE, shadow=True, shadow_opacity=50)
        self.dialog_text = Text((230, 255), "", 32, Colors.SPRITE, shadow=True, shadow_opacity=50)
        self.dialog_text.max_width = 280
        self.dialog_text.pivot = self.dialog_text.Pivot.TOP_LEFT
        self.continue_indicator = Sprite((496, 316), Assets.images_world["continue"])
        self.continue_indicator.pivot = self.continue_indicator.Pivot.TOP_LEFT
        self.dialog_end = False
        self.char_index = 0
        self.render_speed = 25
        self.end_render = False
        self.sound_timer = Timer(0.1)
        self.sound_timer.start()

    @property
    def current_dialog(self) -> Dialog:
        return self.dialogs[self.dialog_index]

    def skip_render(self):
        self.char_index = len(self.current_dialog.current_sentence) - 1
        self.dialog_text.text = self.current_dialog.current_sentence
        self.end_render = True

    def render_text(self):
        if self.end_render:
            return
        if self.char_index >= len(self.current_dialog.current_sentence):
            self.end_render = True
            return
        self.char_index += self.render_speed * Time.dt
        self.dialog_text.text = self.current_dialog.current_sentence[:int(self.char_index)]
        if self.sound_timer.update():
            AudioManager.play_random_from("dialog")
            self.sound_timer.start()

    def update(self):
        if Input.keyboard.keys["space"]:
            if self.end_render and not self.current_dialog.end_dialog:
                self.current_dialog.next_sentence()
                self.char_index = 0
                self.end_render = False
            elif self.end_render and self.current_dialog.end_dialog:
                self.dialog_end = True
            else:
                self.skip_render()
        self.render_text()

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.actor_name.render(display)
        self.dialog_text.render(display)
        if self.end_render:
            self.continue_indicator.render(display)
