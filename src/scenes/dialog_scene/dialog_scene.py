from engine.scene.scene import Scene
from src.scenes.dialog_scene.dialog import DialogBox
from src.scenes.dialog_scene.portrait import Portrait
from src.scenes.world.npc import NPC
from engine.input import Input
from engine.dialog_manager import Dialog
from engine.playerdata import PlayerData


class DialogScene(Scene):
    def __init__(self, npc: NPC, zone, world):
        super().__init__("dialog")
        self.dialog_box = DialogBox(npc, self.choose_dialog(npc).text)
        self.portrait = Portrait(npc.name)
        self.zone = zone
        self.world = world

    @staticmethod
    def choose_dialog(npc: NPC) -> Dialog:
        # Check if npc is the objective of current tasks
        print(f"Choosing dialog of {npc.name}")
        print(f"Looking up the current tasks {PlayerData.tasks.current_tasks}")
        for task in PlayerData.tasks.current_tasks:
            print(f"Reviewing task {task.id}")
            if npc.name.lower() == task.objective:
                # Complete task
                PlayerData.complete_task(task.id)
                # Add new mission to player
                dialog = npc.task_complete_dialog(task.id)
                return dialog
                # If not, return a generic Dialog
        # Check if NPC can give mission
        for dialog in npc.dialogs:
            if dialog.add_mission != "":

                PlayerData.add_task(dialog.add_mission)
                return dialog
        # Check if NPC can give item
        unique_dialog = npc.get_special_dialog()
        if unique_dialog:
            return unique_dialog
        print("Returning generic dialog")
        return npc.generic_dialog()

    def update(self) -> None:
        self.dialog_box.update()
        if Input.keyboard.keys["esc"] or self.dialog_box.dialog_end:
            from engine.scene.scene_manager import SceneManager
            SceneManager.exit_scene()
        self.portrait.update()
        self.zone.dialog_update()
        self.world.notifications.update()

    def render(self) -> None:
        self.zone.render()
        self.display.blit(self.zone.display, (0, 0))
        self.dialog_box.render(self.display)
        self.portrait.render(self.display)
        self.world.render_notifications(self.display)
