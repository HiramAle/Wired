from engine.scene.scene import Scene
from engine.objects.sprite import Sprite
from engine.assets import Assets
from engine.input import Input
from engine.ui.text import Text
from engine.constants import Colors
from engine.loader import Loader


class TestScene(Scene):
    def __init__(self):
        super().__init__("test")
        self.sprite_test = Sprite(self.center, Assets.images_misc["logo"])
        self.text_test = Text(self.center, "Haloooo\nHaloooo", 16, Colors.GREEN)
        self.text_test.pivot = self.text_test.Pivot.MID_BOTTOM
        self.text_test.shadow = True
        self.animation = Assets.animations["loading"]["intro"]

    def update(self) -> None:
        self.text_test.position = Input.mouse.position
        if Input.keyboard.keys["space"]:
            if self.animation.is_playing:
                self.animation.stop()
            else:
                self.animation.play()
        self.animation.update()

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.sprite_test.render(self.display)
        self.text_test.render(self.display)
        self.display.blit(self.animation.current_frame, (100, 100))
