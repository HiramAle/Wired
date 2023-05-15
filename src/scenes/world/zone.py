from engine.window import Window
from engine.input import Input
from engine.data import Data
from engine.scene.scene import Scene
# from src.entities.camera import Camera
from src.scenes.world.camera import Camera
from src.scenes.world.npc import NPC
from src.scenes.world.game_map import GameMap
from src.scenes.world.tiled_object import TiledObject
from src.constants.colors import BLACK_SPRITE
from src.scenes.world.player import Player


class Zone(Scene):
    def __init__(self, name: str, npc_list: list[NPC], before=""):
        super().__init__(name)
        self.map = GameMap(Data.maps[name])
        self.npc_list = [npc for npc in npc_list if npc.current_zone == name]
        self.debug = False
        self.map_colliders = self.map.colliders
        self.map_objects = self.map.objects
        self.map_triggers = self.map.interact
        self.player = Player((0, 0), self.map_colliders, self.map_objects, self.map_triggers)
        self.player.position = self.map.get_position(f"player_{before}").tuple
        self.player.direction = self.map.get_position(f"player_{before}").properties["direction"]
        self.camera = Camera(self.map.width, self.map.height)
        self.camera.actor_tracking = self.player
        self.camera.position = self.player.x - 320, self.player.y - 180
        self.obj: TiledObject | None = None

    def move_objects(self):
        if any([obj.hovered(self.camera.offset) for obj in self.map.objects]):
            Window.set_cursor("hand")
        elif not self.obj:
            Window.set_cursor("arrow")
        if self.obj:
            Window.set_cursor("grab")

        if self.obj:
            self.obj.x = Input.mouse.x - self.obj.rect.width / 2
            self.obj.y = Input.mouse.y - self.obj.rect.height / 2
            if Input.mouse.buttons["left"]:
                x = Input.mouse.x + self.camera.x - self.obj.rect.width / 2
                y = Input.mouse.y + self.camera.y - self.obj.rect.height / 2
                self.obj.x, self.obj.y = x, y
                self.map.objects.append(self.obj)
                self.obj = None
        else:
            for obj in self.map.objects:
                if obj.clicked(self.camera.offset):
                    self.obj = obj
                    self.map.objects.remove(self.obj)
                    break

    def update(self) -> None:
        self.player.update()
        self.camera.update()

        for npc in [npc for npc in self.npc_list if npc.current_zone == self.name]:
            npc.update()

    def render(self) -> None:
        self.display.fill(BLACK_SPRITE)
        self.display.blit(self.map.ground, -self.camera.offset)
        for obj in sorted(
                [self.player] + self.map_objects + [npc for npc in self.npc_list if npc.current_zone == self.name],
                key=lambda sprite: sprite.sort_point):
            obj.render(self.display, self.camera.offset)

        if self.obj:
            self.obj.render(self.display)
