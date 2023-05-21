import sys

import pygame
from os import listdir, rename
from engine.loader import Loader

# for file in listdir("accessories"):
#     slices = file.split(".")[0].split("_")
#     new_name = f"{'_'.join(slices[2:-2])}_{int(slices[-1])}.png"
#     rename(f"accessories/{file}", f"accessories/{new_name}")
pygame.init()
screen = pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()


def import_accessories() -> dict[str, list[pygame.Surface]]:
    path = "accessories"
    animations: dict[str, list[pygame.Surface]] = {}
    rect = pygame.Rect(32 * 3, 0, 32, 64)
    for filename in listdir(path):
        sprite_sheet = pygame.image.load(f"{path}/{filename}").convert_alpha()

        accessory_filename = filename.split(".")[0]
        accessory_name = "_".join(accessory_filename.split("_")[:-1]).lower()
        variation = accessory_filename.split("_")[-1]
        print(accessory_filename, accessory_name, variation)
        icon = pygame.Surface((32, 64), pygame.SRCALPHA)
        icon.blit(sprite_sheet, (0, 0), rect)
        if accessory_name in animations.keys():
            animations[accessory_name].append(icon)
        else:
            animations[accessory_name] = [icon]
    return animations


icons = import_accessories()
icons_names = list(icons.keys())
current_icon = 0

icon_image = icons[icons_names[current_icon]][0]
icon_rect = icon_image.get_rect(center=(50, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                current_icon += 1
                if current_icon >= len(icons_names):
                    current_icon = 0
                icon_image = icons[icons_names[current_icon]][0]

    screen.fill("#2e2e2e")

    screen.blit(icon_image, icon_rect)

    pygame.display.update()
    clock.tick()
