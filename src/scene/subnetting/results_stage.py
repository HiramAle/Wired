from src.scene.core.scene import Stage
from src.scene.subnetting.subnetting_objects import *
from src.gui.image import GUIImage
from src.game_object.sprite import SpriteGroup


class Results(Stage):
    def __init__(self, scene):
        super().__init__("results", scene)
        self.group = SpriteGroup()
        GUIImage("frame", (149, 15), assets.images_subnetting["results_frame"], self.group, centered=False)
        GUIImage("underscore", (179, 65), assets.images_subnetting["results_underscore"], self.group, centered=False)
        GUIText("!RESULTADOS¡", (180, 16), 64, self.group, centered=False)
        GUIText("Tiempo:...", (163, 84), 32, self.group, centered=False)
        GUIText("10:00", (336, 84), 32, self.group, centered=False)

    def update(self) -> None:
        self.group.update()

    def render(self) -> None:
        self.group.render(self.display)
