import sys
import pygame
from src.new_objects.map import Map
from src.new_objects.entity import Group
from src.new_objects.entities import Actor, Player, NPC

pygame.init()
window = pygame.display.set_mode((1280, 720))
canvas = pygame.Surface((640 * 2, 320 * 2))
clock = pygame.time.Clock()
dt = 0.2
path = "../../data/maps/TMX/Village.tmx"
game_map = Map(path)
font = pygame.Font("../../assets/fonts/monogram.ttf", 16)

debug_collision = False

camera_position = pygame.math.Vector2(0, 0)
mouse = pygame.math.Vector2(0, 0)
dragging = False
test = pygame.math.Vector2(0, 0)
offset = pygame.math.Vector2(0, 0)
drag_mode = False

tiled_objects = Group()
tiled_objects.add(*game_map.objects)

obstacles = Group()
obstacles.add(*game_map.obstacles)

player = Player((500, 200), obstacles)

tiled_objects.add(player)
npc = NPC((500, 200), obstacles)
tiled_objects.add(npc)

while True:
    for event in pygame.event.get():
        event: pygame.Event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drag_mode = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.key == pygame.K_LCTRL:
                debug_collision = not debug_collision

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            drag_mode = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if drag_mode:
                    dragging = True
                    offset = mouse.copy()
                else:
                    # player.position = (mouse * 2) - camera_position
                    ...
            if event.button == 2:
                npc.position = (mouse * 2) - camera_position
            if event.button == 3:
                npc.target = (mouse * 2) - camera_position
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drag_mode:
            dragging = False

    mouse.x = int(pygame.mouse.get_pos()[0] / 1280 * 640)
    mouse.y = int(pygame.mouse.get_pos()[1] / 720 * 320)
    if dragging:
        camera_position += mouse - offset
        offset = mouse.copy()

    tiled_objects.update(dt=dt)

    canvas.fill("#2e2e2e")
    canvas.blit(game_map.background, (0 + camera_position.x, 0 + camera_position.y))

    tiled_objects.render_3d(canvas, camera_position)

    if debug_collision:
        for obstacle in obstacles.entities:
            collider = obstacle.collider.copy()
            collider.x += camera_position.x
            collider.y += camera_position.y
            pygame.draw.rect(canvas, "red", collider)
        collider = npc.collider.copy()
        collider.x += camera_position.x
        collider.y += camera_position.y
        pygame.draw.rect(canvas, "blue", collider)

    window.blit(pygame.transform.scale(canvas, (1280, 720)), (0, 0))

    pygame.display.update()
    dt = clock.tick() / 1000
