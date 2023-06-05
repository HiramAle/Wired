from engine.scene.scene import Scene
from src.scenes.dialog_scene.dialog import DialogBox
from src.scenes.dialog_scene.portrait import Portrait
from src.scenes.world.npc import NPC
from engine.input import Input
from engine.dialog_manager import Dialog
from src.scenes.world.key_hint import KeyHint


class DialogScene(Scene):
    def __init__(self, npc: NPC, zone, world):
        super().__init__("dialog")
        self.dialog_box = DialogBox(npc, self.choose_dialog(npc).text)
        self.portrait = Portrait(npc.name)
        self.zone = zone
        self.world = world
        self.key_hint = KeyHint(KeyHint.Type.SKIP)

    @staticmethod
    def choose_dialog(npc: NPC) -> Dialog:
        # Check if npc is the objective of current tasks
        complete_task_dialog = npc.task_complete_dialog()
        if complete_task_dialog:
            return complete_task_dialog
        # Check if NPC can give task
        new_task_dialog = npc.get_new_task_dialog()
        if new_task_dialog:
            return new_task_dialog
        # Check if NPC can give item
        add_item_dialog = npc.get_add_item_dialog()
        if add_item_dialog:
            return add_item_dialog
        print("Returning generic dialog")
        return npc.get_generic_dialog()

    def update(self) -> None:
        self.dialog_box.update()
        if self.dialog_box.dialog_end:
            from engine.scene.scene_manager import SceneManager
            SceneManager.exit_scene()
            self.zone.key_hint.activate()
        self.portrait.update()
        self.zone.dialog_update()
        self.world.notifications.update()

    def render(self) -> None:
        self.zone.render()
        self.display.blit(self.zone.display, (0, 0))
        self.dialog_box.render(self.display)
        self.portrait.render(self.display)
        self.world.render_notifications(self.display)
        self.key_hint.render(self.display)
