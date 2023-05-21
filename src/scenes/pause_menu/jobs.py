from engine.assets import Assets
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, ItemSlot


class Jobs(Scene):
    def __init__(self):
        super().__init__("jobs")
