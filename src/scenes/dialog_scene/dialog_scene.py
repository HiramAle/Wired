from engine.scene.scene import Scene
from src.scenes.dialog_scene.dialog import DialogBox
from src.scenes.dialog_scene.portrait import Portrait
from src.scenes.world.npc import NPC
from engine.input import Input
from engine.dialog_manager import Dialog
from engine.playerdata import PlayerData


class DialogScene(Scene):
    def __init__(self, npc: NPC, zone):
        super().__init__("dialog")
        self.dialog_box = DialogBox(npc, self.choose_dialog(npc).text)
        self.portrait = Portrait(npc.name)

    @staticmethod
    def choose_dialog(npc: NPC) -> Dialog:
        # Check if npc is the objective of current tasks
        print(f"Choosing dialog of {npc.name}")
        print(f"Looking up the current tasks {PlayerData.tasks.current_tasks}")
        for task in PlayerData.tasks.current_tasks:
            print(f"Reviewing task {task.id}")
            if npc.name.lower() == task.objective:
                # Complete task
                task.completed = True
                # Add new mission to player
                dialog = npc.task_complete_dialog(task.id)
                if dialog.new_mission != "":
                    PlayerData.tasks.add_task(dialog.new_mission)
                return dialog
                # If not, return a generic Dialog
        return npc.generic_dialog()

        # if npc.name.lower() not in task.npcs:
        #     return npc.get_generic_dialog()
        #
        # if not npc.name.lower() == task.objective:
        #     return npc.get_dialog(task.id, 1)
        # return npc.get_dialog(task.id, 0)

        # if npc.name.lower() in task.npcs:
        #     if npc.name.lower() == task.objective:
        #         if task.completed:
        #             return npc.get_dialog(task.id, 1)
        #     else:
        #         return npc.get_dialog(task.id, 0)
        # else:
        #     return npc.get_generic_dialog()
        # if npc.name.lower() not in task.npcs:
        #     return npc.get_generic_dialog()
        # if npc.name.lower() == task.objective:
        #     print("Completing task")
        #     task.completed = True
        # if task.completed:
        #     print("Task completed")
        #     return npc.get_dialog(task.id, 1)

    def update(self) -> None:
        self.dialog_box.update()
        if Input.keyboard.keys["esc"] or self.dialog_box.dialog_end:
            from engine.scene.scene_manager import SceneManager
            SceneManager.exit_scene()
        self.portrait.update()

    def render(self) -> None:
        self.dialog_box.render(self.display)
        self.portrait.render(self.display)
