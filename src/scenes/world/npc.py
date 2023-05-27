import pygame
import src.utils.load as load
from engine.assets import Assets
from src.scenes.world.actor import Actor, Emote
from src.constants.paths import NPC_SPRITE_SHEETS, NPC_DATA
from engine.input import Input


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
    def __init__(self, name: str, position: tuple, player: Actor):
        path = f"{NPC_SPRITE_SHEETS}/{name}.png"
        super().__init__(position, path, [])
        self.name = name
        self.data = load.load_json(f"{NPC_DATA}/{name}.json")
        self.route = [(200, 200), (200, 500), (200, 200)]
        self.routes = []
        self.node_index = 0
        self.speed = 100
        self.active_route: Route | None = None
        self.current_zone = self.data["start_zone"]
        self.talkable = False
        self.player = player

    def __repr__(self):
        return f"NPC({self.name}, {self.position})"

    @property
    def player_distance(self) -> float:
        return (self.position - self.player.position).magnitude()

    @property
    def current_node(self) -> tuple | None:
        if self.node_index < len(self.route):
            return self.route[self.node_index]
        return None

    @property
    def target(self) -> pygame.Vector2:
        return pygame.Vector2(self.current_node)

    def interact(self) -> bool:
        if self.player_distance <= 50 and Input.keyboard.keys["interact"]:
            return True

    def pathing(self, daytime: int):
        ...
        # for route in self.routes:
        #     if route.time == int(daytime):
        #         self.active_route = route
        #         break
        # if not self.active_route:
        #     return
        # if self.active_route.finished:
        #     self.active_route.reset()
        #     self.direction = "down"
        #     self.action = "sleep"
        #     self.x, self.y = 255, 222
        #     self.shadow = None
        #     self.active_route = None
        #     self.paused = False
        #     return
        # self.movement = self.active_route.target - self.position
        # if self.movement.magnitude() < 1:
        #     self.position = self.active_route.target
        #     self.movement.x, self.movement.y = 0, 0
        #     self.active_route.next()

    def update(self):
        self.update_status()
        self.animate()
        self.move()
