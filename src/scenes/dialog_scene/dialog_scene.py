from engine.scene.scene import Scene
from src.scenes.dialog_scene.dialog import DialogBox
from src.scenes.world.npc import NPC
from engine.input import Input


class DialogScene(Scene):
    def __init__(self, npc: NPC):
        super().__init__("dialog")
        self.dialog_box = DialogBox(npc)

    def update(self) -> None:
        self.dialog_box.update()
        if Input.keyboard.keys["esc"] or self.dialog_box.dialog_end:
            from engine.scene.scene_manager import SceneManager
            SceneManager.exit_scene()

    def render(self) -> None:
        self.dialog_box.render(self.display)