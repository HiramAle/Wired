import pygame
from engine.objects.sprite import Sprite
from src.scenes.world.npc import NPC
from engine.assets import Assets
from engine.ui.text import Text
from engine.constants import Colors
from engine.input import Input
from engine.time import Time
from engine.save_manager import instance as save_manager


class Dialog:
    def __init__(self, dialog_id: int, sentences: list[str]):
        self.id = dialog_id
        self.sentences = sentences
        self.sentence_index = 0

    @property
    def end_dialog(self) -> bool:
        return self.sentence_index >= len(self.sentences) - 1

    @property
    def current_sentence(self) -> str:
        return self.sentences[self.sentence_index].replace("@", save_manager.active_save.name)

    def next_sentence(self):
        self.sentence_index += 1


class DialogBox(Sprite):
    def __init__(self, npc: NPC):
        super().__init__((127, 246), Assets.images_world["dialog_box"])
        self.pivot = self.Pivot.TOP_LEFT
        self.dialogs = [Dialog(dialog_id, dialog_list) for dialog_id, dialog_list in npc.data["dialogs"].items()]
        self.dialog_index = 0
        self.npc = npc
        self.actor_name = Text((157, 325), npc.name, 32, Colors.SPRITE)
        self.actor_name.pivot = self.actor_name.Pivot.TOP_LEFT
        self.dialog_text = Text((222, 262), "", 32, Colors.SPRITE)
        self.dialog_text.max_width = 300
        self.dialog_text.pivot = self.dialog_text.Pivot.TOP_LEFT
        self.continue_indicator = Sprite((496, 316), Assets.images_world["continue"])
        self.continue_indicator.pivot = self.continue_indicator.Pivot.TOP_LEFT
        self.dialog_end = False
        self.char_index = 0
        self.render_speed = 25
        self.end_render = False

    @property
    def current_dialog(self) -> Dialog:
        return self.dialogs[self.dialog_index]

    def skip_render(self):
        self.char_index = len(self.current_dialog.current_sentence) - 1
        self.dialog_text.text = self.current_dialog.current_sentence[:int(self.char_index)]
        self.end_render = True

    def render_text(self):
        if self.end_render:
            return
        if self.char_index >= len(self.current_dialog.current_sentence):
            self.end_render = True
            return
        self.char_index += self.render_speed * Time.dt
        self.dialog_text.text = self.current_dialog.current_sentence[:int(self.char_index)]

    def update(self):
        if Input.keyboard.keys["space"]:
            if self.end_render and not self.current_dialog.end_dialog:
                print("End rendering but not end of dialog")
                self.current_dialog.next_sentence()
                self.char_index = 0
                self.end_render = False
            elif self.end_render and self.current_dialog.end_dialog:
                print("End rendering and end of dialog")
                self.dialog_end = True
            else:
                print("Skip dialog render")
                self.skip_render()

        self.render_text()

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.actor_name.render(display)
        self.dialog_text.render(display)
        if self.end_render:
            self.continue_indicator.render(display)
