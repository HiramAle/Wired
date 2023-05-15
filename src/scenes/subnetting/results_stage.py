from engine.scene.scene import Stage
from src.scenes.subnetting.subnetting_objects import *
from engine.ui.image import Image
from engine.ui.text import Text
from engine.objects.sprite import SpriteGroup
from engine.assets import Assets


class Results(Stage):
    def __init__(self, scene, time: float):
        super().__init__("results", scene)
        self.group = SpriteGroup()
        self.time_elapsed = time
        Image((149, 15), Assets.images_subnetting["results_frame"], self.group, centered=False)
        Image((179, 65), Assets.images_subnetting["results_underscore"], self.group, centered=False)
        Text((180, 16), "¡RESULTADOS!", 64, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((163, 84), "Tiempo:...", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((336, 84), self.time_string(), 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((163, 212), "Dinero obtenido......", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        self.instructions = Text((320, 334), "Presiona espacio para continuar", 16, "#2E2E2E", self.group, shadow=False)
        self.instructions.image.set_alpha(int(255 * .75))

    def time_string(self):
        minutes = int(self.time_elapsed / 60)
        seconds = int(self.time_elapsed % 60)
        time_string = "{:02d}:{:02d}".format(minutes, seconds)
        return time_string

    def update(self) -> None:
        self.group.update()

    def render(self) -> None:
        self.group.render(self.display)
