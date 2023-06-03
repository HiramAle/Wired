import pygame
from engine.assets import Assets
from engine.time import Time
from engine.loader import Loader
from engine.objects.sprite import Sprite


class Portrait(Sprite):
    def __init__(self, npc: str):
        super().__init__((178, 295), pygame.Surface((64, 64), pygame.SRCALPHA))
        self.frames = Assets.portrait_frames[npc.title()]["talk"]
        self.animation_speed = 10
        self.frame_index = 0

    def update(self, *args, **kwargs):
        self.frame_index += self.animation_speed * Time.dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


class PlayerPortrait(Sprite):
    def __init__(self):
        super().__init__((45, 45), pygame.Surface((64, 64), pygame.SRCALPHA))
        from engine.save_manager import instance as save_manager
        self.animations = Loader.load_portrait_frames(save_manager.active_save.portrait, 64)
        self.animation_speed = 10
        self.frame_index = 0
        self.__status = "idle"
        self.frames = self.animations["talk"]
        self.image = self.animations["talk"][0]

    def update(self, *args, **kwargs):
        if self.__status == "idle":
            return
        self.frame_index += self.animation_speed * Time.dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in ["talk", "nod", "shake", "idle"]:
            print(f"Portrait doesn't have {value} status")
            return
        if value == "idle":
            self.image = self.animations["talk"][0]
        self.__status = value


def save_portrait(body_type: int, eyes_color: int, hairstyle_type: int, hairstyle_color: int):
    body_path = f"assets/portrait_generator/bodies/body_{body_type}.png"
    eyes_path = f"assets/portrait_generator/eyes/eye_{eyes_color}.png"
    hairstyles_path = f"assets/portrait_generator/hairstyles/hairstyle_{hairstyle_type}_{hairstyle_color}.png"

    try:
        body_image = Loader.load_image(body_path)
        eyes_image = Loader.load_image(eyes_path)
        hairstyle_image = Loader.load_image(hairstyles_path)
    except FileNotFoundError:
        print("File Not Found")
    else:
        portrait_sprite_sheet = pygame.Surface(body_image.get_size(), pygame.SRCALPHA)

        portrait_sprite_sheet.blit(body_image, (0, 0))
        portrait_sprite_sheet.blit(hairstyle_image, (0, 0))
        portrait_sprite_sheet.blit(eyes_image, (0, 0))

        from engine.save_manager import instance as save_manager
        pygame.image.save(portrait_sprite_sheet, save_manager.active_save.portrait)
