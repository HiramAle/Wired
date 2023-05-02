import sys
import pygame
import pytmx

pygame.init()
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Map editor")
canvas = pygame.Surface((1280, 720))
clock = pygame.time.Clock()
dt = 0.2
mouse = pygame.math.Vector2(0, 0)

font = pygame.Font("../../assets/fonts/monogram.ttf", 32)

tiled_map = pytmx.load_pygame("../../data/maps/TMX/Casa_custom.tmx", pixelalpha=True)
layers: dict[str, pygame.Surface] = {}

for layer in tiled_map.layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        image = pygame.Surface((tiled_map.width * 32, tiled_map.height * 32), pygame.SRCALPHA)
        for x, y, gid in layer:
            tile = tiled_map.get_tile_image_by_gid(gid)
            if tile:
                image.blit(tile, (x * 32, y * 32))
        layers[layer.name] = image

image = pygame.image.load("Casa_custom.png").convert_alpha()
layers["tile_set"] = image

active_layer = list(layers.keys())[0]
layer_index = 0

pan_active = False
panning = False
pan_offset = pygame.Vector2(0, 0)
offset = pygame.Vector2(0, 0)

image_grid = pygame.Surface(image.get_size(), pygame.SRCALPHA)

selection: None | pygame.Rect = None
export_index = 0
tiles = []

for y in range(0, 30 * 32, 32):
    pygame.draw.line(image_grid, "white", (0, y), (image.get_width(), y))

for x in range(0, 30 * 32, 32):
    pygame.draw.line(image_grid, "white", (x, 0), (x, image.get_height()))

while True:
    for event in pygame.event.get():
        event: pygame.Event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pan_active = True
            if event.key == pygame.K_LSHIFT:
                if selection:
                    selection = None
                else:
                    min_x = min([tile.x for tile in tiles])
                    min_y = min([tile.y for tile in tiles])
                    max_x = max([tile.x for tile in tiles])
                    max_y = max([tile.y for tile in tiles])

                    width = max_x - min_x + 32
                    height = max_y - min_y + 32

                    selection = pygame.Rect(min_x, min_y, width, height)
            if event.key == pygame.K_LCTRL:
                if tiles:
                    min_x = min([tile.x for tile in tiles])
                    min_y = min([tile.y for tile in tiles])
                    max_x = max([tile.x for tile in tiles])
                    max_y = max([tile.y for tile in tiles])

                    width = max_x - min_x + 32
                    height = max_y - min_y + 32

                    selection = pygame.Rect(min_x, min_y, width, height)
                    image_selection = pygame.Surface(selection.size, pygame.SRCALPHA)
                    image_selection.blit(layers[active_layer], (0, 0), selection)
                    pygame.image.save(image_selection, f"export_{export_index}.png")
                    export_index += 1
            if event.key == pygame.K_ESCAPE:
                tiles = []
                selection = None

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pan_active = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x = ((mouse.x - pan_offset.x) // 32) * 32
            y = ((mouse.y - pan_offset.y) // 32) * 32
            if event.button == 1:
                if pan_active:
                    panning = True
                    offset = mouse.copy()
                else:
                    rect = pygame.Rect(x, y, 32, 32)
                    if rect not in tiles:
                        tiles.append(rect)
            if event.button == 3:
                rect = pygame.Rect(x, y, 32, 32)
                if rect in tiles:
                    tiles.remove(rect)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pan_active:
                    panning = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                layer_index += 1
            else:
                layer_index -= 1
            if layer_index >= len(layers):
                layer_index = len(layers) - 1
            elif layer_index < 0:
                layer_index = 0
            active_layer = list(layers.keys())[layer_index]

    mouse.x, mouse.y = pygame.mouse.get_pos()

    if panning:
        pan_offset += mouse - offset
        offset = mouse.copy()

    canvas.fill("#2e2e2e")

    canvas.blit(layers[active_layer], (0, 0) + pan_offset)
    canvas.blit(image_grid, (0, 0) + pan_offset)

    for tile in tiles:
        offset_tile = tile.copy()
        offset_tile.x += pan_offset.x
        offset_tile.y += pan_offset.y
        img = pygame.Surface((32, 32), pygame.SRCALPHA)
        img.fill((255, 255, 255, 100))
        canvas.blit(img, offset_tile)

    if selection:
        img = pygame.Surface(selection.size, pygame.SRCALPHA)
        img.fill((255, 0, 0, 100))
        offset_selection = selection.copy()
        offset_selection.x += pan_offset.x
        offset_selection.y += pan_offset.y
        canvas.blit(img, offset_selection)

    canvas.blit(font.render(active_layer, False, "white"), (10, 10))
    window.blit(pygame.transform.scale(canvas, (1280, 720)), (0, 0))

    pygame.display.update()
    dt = clock.tick() / 1000
