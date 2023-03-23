from src.scene.scene import Scene
from src.gui.image import GUIImage
from src.gui.text import GUIText
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.game_object.sprite import SpriteGroup
import src.engine.assets as assets


class Selector(Scene):
    def __init__(self):
        super().__init__("selector")
        self.group = SpriteGroup()
        self.cables = GUIImage("cables", (CANVAS_WIDTH / 4, CANVAS_HEIGHT / 3), assets.images_selector["cables"],
                               self.group)
        self.routing = GUIImage("routing", (CANVAS_WIDTH / 4 * 2, CANVAS_HEIGHT / 3), assets.images_selector["routing"],
                                self.group)
        self.subnetting = GUIImage("cables", (CANVAS_WIDTH / 4 * 3, CANVAS_HEIGHT / 3),
                                   assets.images_selector["subnetting"], self.group)
        GUIText("Cables", (CANVAS_WIDTH / 4, 110), 32, self.group)
        GUIText("Subnetting", (CANVAS_WIDTH / 4 * 2, 110), 32, self.group)
        GUIText("Routing", (CANVAS_WIDTH / 4 * 3, 110), 32, self.group)

    def render(self) -> None:
        ...
