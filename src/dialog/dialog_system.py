import pygame
import engine.assets as assets
import engine.input as game_input
import engine.time as game_time
from engine.objects.sprite import Sprite


class DialogBox(Sprite):
    def __init__(self, position: tuple, *groups, **kwargs):
        image = pygame.Surface((400, 100))
        super().__init__(self.__class__.__name__, position, image, *groups, **kwargs)
        self.text = ""
        self.character = 0
        self.speed = 10

    def render(self, display: pygame.Surface, offset=(0, 0)):
        super().render(display, offset)
        self.character += self.speed * game_time.dt
        if self.character >= len(self.text):
            self.character = len(self.text)
        text_surface = assets.fonts["monogram"].render(self.text[:int(self.character)], 32)
        text_rect = text_surface.get_rect(center=self.rect.center)
        display.blit(text_surface, text_rect)


class DialogManager:
    def __init__(self, screen):
        self.screen = screen
        self.dialogs = []
        self.current_dialog: DialogBox | None = None

    def show_dialog(self, *texts):
        for text in texts:
            dialog = DialogBox((320, 300))
            dialog.text = text
            self.dialogs.append(dialog)
        self.current_dialog = self.dialogs[0]

    def next_dialog(self):
        if len(self.dialogs) > 1:
            self.dialogs.pop(0)
            self.current_dialog = self.dialogs[0]
        else:
            self.current_dialog = None

    def close_dialog(self):
        self.dialogs.clear()
        self.current_dialog = None

    def render(self):
        if self.current_dialog:
            self.current_dialog.render(self.screen)

    def update(self):
        if self.current_dialog:
            if game_input.keyboard.keys["space"]:
                self.next_dialog()
            elif game_input.keyboard.keys["esc"]:
                self.close_dialog()
