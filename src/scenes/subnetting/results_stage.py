from engine.scene.scene import Stage
from src.scenes.subnetting.subnetting_objects import *
from engine.ui.image import Image
from engine.ui.text import Text
from engine.objects.sprite import SpriteGroup
from engine.assets import Assets
from engine.playerdata import PlayerData


class Results(Stage):
    def __init__(self, scene, time: float, crossover_used: list[int], straight_used: list[int]):
        super().__init__("results", scene)
        self.group = SpriteGroup()
        self.time_elapsed = time

        quality_3 = (crossover_used + straight_used).count(3)
        quality_2 = (crossover_used + straight_used).count(2)
        quality_1 = (crossover_used + straight_used).count(1)

        payment = 0

        if time <= 60:
            time_bonus = 50
        elif time <= 120:
            time_bonus = 30
        else:
            time_bonus = 10

        for quality in crossover_used + straight_used:
            payment += quality * 10

        payment += time_bonus

        Image((149, 15), Assets.images_subnetting["results_frame"], self.group, centered=False)
        Image((179, 65), Assets.images_subnetting["results_underscore"], self.group, centered=False)
        Text((180, 16), "¡RESULTADOS!", 64, "#2E2E2E", self.group, centered=False, shadow=False)
        # Time
        Text((163, 84), "Tiempo...", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((360, 84), self.time_string(), 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((420, 84), f"+${time_bonus}", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        # Quality 3
        Text((163, 110), f"Cables usados...", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((360, 110), str(quality_3), 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((420, 110), f"+${30 * quality_3}", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        # Quality 2
        Text((163, 138), f"Cables usados...", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((360, 138), str(quality_2), 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((420, 138), f"+${20 * quality_2}", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        # Quality 1
        Text((163, 164), f"Cables usados...", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((360, 164), str(quality_1), 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((420, 164), f"+${10 * quality_1}", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        # Payment
        Text((163, 212), f"Dinero ganado...", 32, "#2E2E2E", self.group, centered=False, shadow=False)
        Text((420, 212), f"+${payment}", 32, "#2E2E2E", self.group, centered=False, shadow=False)

        self.instructions = Text((320, 334), "Presiona espacio para continuar", 16, "#2E2E2E", self.group, shadow=False)
        self.instructions.image.set_alpha(int(255 * .75))

        PlayerData.inventory.money += payment

    def time_string(self):
        minutes = int(self.time_elapsed / 60)
        seconds = int(self.time_elapsed % 60)
        time_string = "{:02d}:{:02d}".format(minutes, seconds)
        return time_string

    def update(self) -> None:
        self.group.update()

    def render(self) -> None:
        self.group.render(self.display)
