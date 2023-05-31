import pygame
from engine.assets import Assets
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.ui.text import Text
from engine.constants import Colors


class Marker(Sprite):
    def __init__(self, zone: str, position: tuple, name: str, before: str, *groups):
        super().__init__(position, Assets.images_book["pin"], *groups)
        self.before = before
        self.zone = zone
        self.x += 8
        zone_position = self.rect.centerx, self.rect.centery + 30
        self.zone_text = Text(zone_position, name, 32, Colors.WHITE, shadow=True, shadow_opacity=125,
                              shadow_color=Colors.SPRITE)
        self.outline_color = Colors.WHITE
        self.outline_width = 3

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        if self.pivot == self.Pivot.CENTER:
            rect = surface.get_rect(center=self.position)
        elif self.pivot == self.Pivot.TOP_LEFT:
            rect = surface.get_rect(topleft=self.position)

        display.blit(surface, (rect.left + self.outline_width, rect.top))
        display.blit(surface, (rect.left - self.outline_width, rect.top))
        display.blit(surface, (rect.left, rect.top + self.outline_width))
        display.blit(surface, (rect.left, rect.top - self.outline_width))

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.hovered:
            self.draw_outline(display)
        super().render(display, offset)
        self.zone_text.render(display, offset)


class Map(Scene):
    def __init__(self, change_zone: callable):
        super().__init__("map")
        self.map = SpriteGroup()
        Sprite((4, 0), Assets.images_book["map"], self.map, centered=False)
        self.zones = {"players_house": {"position": (238, 79), "name": "Casa", "zone": "village"},
                      "company": {"position": (478, 94), "name": "Routed\nInc", "zone": "city"},
                      "store": {"position": (114, 134), "name": "Tienda", "zone": "village"},
                      "chenchos_house": {"position": (97, 253), "name": "Casa\nChencho", "zone": "village"}}
        self.markers = SpriteGroup()
        self.change_zone = change_zone

        for zone, data in self.zones.items():
            Marker(data["zone"], data["position"], data["name"], zone, self.markers)

    def update(self) -> None:
        for marker in self.markers.sprites():
            marker: Marker
            if marker.clicked and self.change_zone:
                self.change_zone(marker.zone, marker.before)
                from engine.scene.scene_manager import SceneManager
                SceneManager.exit_scene()

    def render(self) -> None:
        self.display = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.map.render(self.display)
        self.markers.render(self.display)
