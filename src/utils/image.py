import pygame


def load_sprite_sheet(sprite_sheet: pygame.Surface, data: dict) -> list[pygame.Surface]:
    sprite_width = data["width"]
    sprite_height = data["height"]
    image = sprite_sheet.convert_alpha()
    tile_num_x = image.get_size()[0] // sprite_width
    tile_num_y = image.get_size()[1] // sprite_height
    print(tile_num_x)
    print(tile_num_y)
    cut_images = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * sprite_width
            y = row * sprite_height
            cut = pygame.Surface((sprite_width, sprite_height))
            cut.set_colorkey(0)
            cut = cut.convert_alpha()
            cut.blit(image, (0, 0), pygame.Rect(x, y, sprite_width, sprite_height))
            cut_images.append(cut)

    return cut_images
