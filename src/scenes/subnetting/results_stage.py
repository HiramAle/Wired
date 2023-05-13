from engine.scene.scene import Stage
from src.scenes.subnetting.subnetting_objects import *
from src.gui.image import GUIImage
from engine.objects.sprite import SpriteGroup


class Results(Stage):
    def __init__(self, scene, time: float):
        super().__init__("results", scene)
        print("Enter results")
        self.group = SpriteGroup()
        self.time_elapsed = time
        GUIImage("frame", (149, 15), assets.images_subnetting["results_frame"], self.group, centered=False)
        GUIImage("underscore", (179, 65), assets.images_subnetting["results_underscore"], self.group, centered=False)
        GUIText("¡RESULTADOS!", (180, 16), 64, self.group, centered=False, color="#2E2E2E", shadow=False)
        GUIText("Tiempo:...", (163, 84), 32, self.group, centered=False, color="#2E2E2E", shadow=False)
        GUIText(self.time_string(), (336, 84), 32, self.group, centered=False, color="#2E2E2E", shadow=False)
        GUIText("Dinero obtenido......", (163, 212), 32, self.group, centered=False, color="#2E2E2E", shadow=False)
        self.instructions = GUIText("Presiona espacio para continuar", (320, 334), 16, self.group,
                                    color="#2E2E2E", shadow=False)
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
