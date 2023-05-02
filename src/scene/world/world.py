from __future__ import annotations

import math

import pygame
import pytmx
import src.engine.time as game_time
import src.engine.data as game_data
import src.engine.input as game_input
import src.engine.assets as game_assets
import src.engine.window as window
import src.utils.load as load
from src.utils.json_saver import instance as save_manager
from src.scene.core.scene_manager import Scene
from src.constants.paths import USER_DATA, NPC_SPRITE_SHEETS, NPC_DATA
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.entities.camera import Camera
from src.constants.colors import BLACK_SPRITE


class Trigger(pygame.Rect):
    def __init__(self, name: str, x: float, y: float, width: float, height: float):
        super().__init__(x, y, width, height)
        self.name = name


class Sprite:
    def __init__(self, position: tuple, image: pygame.Surface):
        self._position = pygame.math.Vector2(position)
        self.image = image

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)) -> None:
        rect = self.rect
        rect.x -= offset.x
        rect.y -= offset.y
        display.blit(self.image, rect)

    def update(self):
        ...

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(center=self._position)

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, value: tuple[float, float]) -> None:
        self._position.x, self._position.y = value

    @property
    def x(self) -> float:
        return self._position.x

    @x.setter
    def x(self, value: float) -> None:
        self._position.x = value

    @property
    def y(self) -> float:
        return self._position.y

    @y.setter
    def y(self, value: float) -> None:
        self._position.y = value

    def hovered(self, offset: pygame.Vector2) -> bool:
        mouse = pygame.Vector2(game_input.mouse.position) + offset
        if self.rect.collidepoint(mouse):
            return True
        return False

    def clicked(self, offset: pygame.Vector2) -> bool:
        mouse = pygame.Vector2(game_input.mouse.position) + offset
        if self.rect.collidepoint(mouse) and game_input.mouse.buttons["left"]:
            return True
        return False


class TiledObject(Sprite):
    def __init__(self, position: tuple, image: pygame.Surface, collider: pygame.Rect | None):
        super().__init__(position, image)
        self._collider = collider

    def __repr__(self):
        return f"TiledObject {self.position}"

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(topleft=self._position)

    @property
    def collider(self) -> pygame.Rect | None:
        if not self._collider:
            return None
        collider = self._collider.copy()
        collider.x += self.x
        collider.y += self.y
        return collider


class Actor(Sprite):
    def __init__(self, position: tuple, sprite_sheet_path: str, collisions: list[pygame.Rect]):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        animations = load.export_animation_frames(sprite_sheet)
        super().__init__(position, animations["idle"]["down"][0])
        self.collisions = collisions
        # Movement attributes
        self._position = pygame.Vector2(position)
        self.speed = 150
        self.movement = pygame.Vector2()
        # Animation attributes
        self.animations = animations
        self.direction = "down"
        self.action = "idle"
        self.frame_index = 0
        self.animation_speed = 10
        # Extra attributes
        self.shadow = game_assets.images_actors["actor_shadow"]
        self.collider = pygame.Rect(0, 0, 28, 20)

    def update_status(self):
        if self.movement.magnitude() > 0:
            self.action = "walk"
            if self.movement.x < 0:
                self.direction = "left"
            if self.movement.x > 0:
                self.direction = "right"
            if self.movement.x == 0:
                if self.movement.y < 0:
                    self.direction = "up"
                if self.movement.y > 0:
                    self.direction = "down"
        elif self.action == "walk":
            self.action = "idle"

    def move(self):
        if self.movement.magnitude() > 1:
            self.movement = self.movement.normalize()
        self.x += self.movement.x * self.speed * game_time.dt
        self.collider.centerx = self.x
        self.collision("x")
        self.y += self.movement.y * self.speed * game_time.dt
        self.collider.bottom = self.rect.bottom
        self.collision("y")

    def animate(self):
        self.frame_index += game_time.dt * self.animation_speed
        if self.frame_index >= len(self.animations[self.action][self.direction]):
            self.frame_index = 0

        self.image = self.animations[self.action][self.direction][int(self.frame_index)]

    def collision(self, axis: str):
        # Change collider if statement and collider collision axis
        for obstacle in [collider for collider in self.collisions if self.collider.colliderect(collider)]:
            if axis == "x":
                if self.movement.x > 0:
                    self.collider.right = obstacle.left
                if self.movement.x < 0:
                    self.collider.left = obstacle.right
                self.x = self.collider.centerx
            if axis == "y":
                if self.movement.y > 0:
                    self.collider.bottom = obstacle.top
                if self.movement.y < 0:
                    self.collider.top = obstacle.bottom

                rect = self.rect
                rect.bottom = self.collider.bottom
                self.y = rect.centery

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.shadow:
            shadow_rect = self.shadow.get_rect()
            shadow_rect.centerx = self.x - offset.x
            shadow_rect.centery = self.rect.bottom - 2 - offset.y
            display.blit(self.shadow, shadow_rect)
        super().render(display, offset)


class Route:
    def __init__(self, name: str, nodes: list, zone: str, time: int):
        self.name = name
        self.nodes: list[tuple[float, float]] = nodes
        self.zone = zone
        self.time = time
        self._index = 0

    @property
    def finished(self) -> bool:
        return self._index >= len(self.nodes)

    @property
    def target(self) -> pygame.Vector2:
        return pygame.Vector2(self.nodes[self._index])

    def next(self):
        self._index += 1

    def reset(self):
        self._index = 0


class NPC(Actor):
    def __init__(self, name: str, position: tuple):
        path = f"{NPC_SPRITE_SHEETS}/{name}.png"
        super().__init__(position, path, [])
        self.name = name
        self.data = load.load_json(f"{NPC_DATA}/{name}.json")
        self.route = [(200, 200), (200, 500), (200, 200)]
        self.routes = [
            Route("sleep", [(384, 585), (384, 300), (330, 300), (330, 240), (300, 240)], "playershouse", 380)]
        self.node_index = 0
        self.speed = 100
        self.active_route: Route | None = None

    @property
    def current_node(self) -> tuple | None:
        if self.node_index < len(self.route):
            return self.route[self.node_index]
        return None

    @property
    def target(self) -> pygame.Vector2:
        return pygame.Vector2(self.current_node)

    def pathing(self, daytime: int):
        for route in self.routes:
            if route.time == int(daytime):
                self.active_route = route
                break
        if not self.active_route:
            return
        if self.active_route.finished:
            self.active_route.reset()
            self.direction = "down"
            self.action = "sleep"
            self.x, self.y = 255, 222
            self.shadow = None
            self.active_route = None
            return
        self.movement = self.active_route.target - self.position
        if self.movement.magnitude() < 1:
            self.position = self.active_route.target
            self.movement.x, self.movement.y = 0, 0
            self.active_route.next()
        self.move()
        # if not self.current_node:
        #     return
        # self.movement = self.target - self.position
        # if self.movement.magnitude() < 1:
        #     self.position = self.target
        #     self.movement.x, self.movement.y = 0, 0
        #     self.node_index += 1
        # self.move()

    def update(self):
        self.update_status()
        self.animate()


class Player(Actor):
    def __init__(self, position: tuple, collisions: list[pygame.Rect], interactions: list[Trigger]):
        path = f"{USER_DATA}/saves/save_{save_manager.index}/sprite_sheet.png"
        super().__init__(position, path, collisions)
        self.interactions = interactions
        self.active_trigger: None | Trigger = None

    def __repr__(self):
        return f"Player {self.position}"

    def input(self):
        # Movement input
        self.movement.x, self.movement.y = 0, 0
        if game_input.keyboard.keys["left"]:
            self.movement.x = - 1
        if game_input.keyboard.keys["right"]:
            self.movement.x = 1
        if game_input.keyboard.keys["up"]:
            self.movement.y = - 1
        if game_input.keyboard.keys["down"]:
            self.movement.y = 1

        if self.active_trigger:
            if game_input.keyboard.keys["interact"]:
                print(self.active_trigger.name)

    def check_triggers(self):
        if self.active_trigger:
            if not self.collider.colliderect(self.active_trigger):
                self.active_trigger = None
            return
        for trigger in self.interactions:
            if self.collider.colliderect(trigger):
                self.active_trigger = trigger
                return

    def update(self):
        self.input()
        self.move()
        self.update_status()
        self.animate()
        self.check_triggers()


class World(Scene):
    def __init__(self):
        super().__init__("world")
        # Day and time
        self.day_time = 360
        self.day_speed = 1.4
        self.week_day = 0
        # Daytime transition
        self.sky_surface = pygame.Surface(self.display.get_size())
        self.day_color = [255, 255, 255]
        self.night_color = (38, 101, 189)
        # Actors
        # self.player = Player()
        self.npc_list = [NPC("kat", (0, 0))]
        self.zone = Zone("playershouse", self.npc_list)
        self.overlay = game_assets.images_world["overlay"]
        self.hour = Sprite((78 + 16, 32), pygame.Surface((1, 1)))
        self.zone.npc_list[0].x, self.zone.npc_list[0].y = self.zone.map.positions["kat"]

    def time_string(self):
        hours = int(self.day_time / 60)
        minutes = (int(self.day_time % 60) // 10) * 10
        time_string = "{:02d}:{:02d}".format(hours, minutes)
        return time_string

    def update(self):
        # Day and time
        self.day_time += self.day_speed * game_time.dt
        if self.day_time >= 1320:
            self.day_time = 360
            self.week_day += 1
            if self.week_day > 6:
                self.week_day = 0
        # Daytime transition
        if self.day_time >= 1200:
            for index, value in enumerate(self.night_color):
                if self.day_color[index] > value:
                    self.day_color[index] -= 2 * game_time.dt
        for npc in self.npc_list:
            npc.pathing(self.day_time)

        self.zone.update()

    def render(self) -> None:
        # Render zone
        self.zone.render()
        self.display.blit(self.zone.display, (0, 0))
        # Daytime transition
        self.sky_surface.fill(self.day_color)
        self.display.blit(self.sky_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.display.blit(self.overlay, (16, 16))
        self.hour.image = game_assets.fonts["monogram"].render(self.time_string(), 16, BLACK_SPRITE)
        self.hour.render(self.display)


class GameMap:
    def __init__(self, map_data: pytmx.TiledMap):
        self.data = map_data
        # Map dimensions
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight
        self.tile_width = self.data.tilewidth
        self.tile_height = self.data.tileheight
        # Map objects
        self.ground = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.player_position = 0, 0
        self.objects_layers = [layer for layer in self.data.layers if isinstance(layer, pytmx.TiledObjectGroup)]
        self.tiled_layers = [layer for layer in self.data.layers if isinstance(layer, pytmx.TiledTileLayer)]
        self.colliders: list[pygame.Rect] = []
        self.interact: list[Trigger] = []
        self.objects: list[TiledObject] = []
        self.positions: dict[str, tuple] = {}

        self.setup()

    def setup(self):
        # Draw ground
        for layer in self.tiled_layers:
            for x, y, gid in layer:
                if not gid:
                    continue
                tile_image = self.data.get_tile_image_by_gid(gid)
                self.ground.blit(tile_image, (x * self.tile_width, y * self.tile_height))
        # Get objects
        for layer in self.objects_layers:
            for tiled_object in layer:
                tiled_object: pytmx.TiledObject
                if layer.name == "collision":
                    collider = pygame.Rect(tiled_object.x, tiled_object.y, tiled_object.width, tiled_object.height)
                    self.colliders.append(collider)
                    continue
                if layer.name == "interactions":
                    interact = Trigger(tiled_object.name, tiled_object.x, tiled_object.y, tiled_object.width,
                                       tiled_object.height)
                    self.interact.append(interact)
                    continue
                if layer.name == "positions":
                    self.positions[tiled_object.name] = (tiled_object.x, tiled_object.y)
                    continue
                image = tiled_object.image
                if not image:
                    continue
                position = tiled_object.x, tiled_object.y
                properties = tiled_object.properties
                # TODO: Add collider list for TiledObject
                colliders = tiled_object.properties["colliders"] if "colliders" in properties else None
                collider = None
                if colliders:
                    collider = colliders[0]
                    collider = pygame.Rect(collider.x, collider.y, collider.width, collider.height)
                self.objects.append(TiledObject(position, image, collider))
        # Get player start position or player enter instead
        # self.player_position = self.positions["player_start"] if self.start else self.positions["player_enter"]


class Zone(Scene):
    def __init__(self, name: str, npc_list: list[NPC], before=""):
        super().__init__(name)
        self.map = GameMap(game_data.maps[name])
        self.npc_list = npc_list
        self.debug = False
        self.colliders = self.map.colliders + [obj.collider for obj in self.map.objects if obj.collider]
        self.player = Player(self.map.positions[f"player_{before}"], self.colliders, self.map.interact)
        self.camera = Camera(self.map.width, self.map.height)
        self.camera._entity = self.player
        self.obj: TiledObject | None = None

    def move_objects(self):
        if any([obj.hovered(self.camera.position_vector) for obj in self.map.objects]):
            window.set_cursor("hand")
        elif not self.obj:
            window.set_cursor("arrow")
        if self.obj:
            window.set_cursor("grab")

        if self.obj:
            self.obj.x = game_input.mouse.x - self.obj.rect.width / 2
            self.obj.y = game_input.mouse.y - self.obj.rect.height / 2
            if game_input.mouse.buttons["left"]:
                x = game_input.mouse.x + self.camera.x - self.obj.rect.width / 2
                y = game_input.mouse.y + self.camera.y - self.obj.rect.height / 2
                self.obj.x, self.obj.y = x, y
                self.map.objects.append(self.obj)
                self.colliders = self.map.colliders + [obj.collider for obj in self.map.objects]
                self.player.collisions = self.colliders
                self.obj = None
        else:
            for obj in self.map.objects:
                if obj.clicked(self.camera.position_vector):
                    self.obj = obj
                    self.map.objects.remove(self.obj)
                    break

    def update(self) -> None:
        self.move_objects()
        self.player.update()
        self.camera.update()

        for npc in self.npc_list:
            npc.update()

    def render(self) -> None:
        self.display.fill(BLACK_SPRITE)
        self.display.blit(self.map.ground, (-self.camera.x, -self.camera.y))
        for obj in sorted([self.player] + [*self.map.objects], key=lambda sprite: sprite.rect.centery):
            obj.render(self.display, self.camera.position_vector)

        for npc in self.npc_list:
            npc.render(self.display, self.camera.position_vector)

        if self.obj:
            self.obj.render(self.display)
