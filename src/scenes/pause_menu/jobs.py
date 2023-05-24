from engine.assets import Assets
from engine.save_manager import instance as save_manager
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, ItemSlot
from src.scenes.world.tasks import TaskManager


class Jobs(Scene):
    def __init__(self):
        super().__init__("jobs")
        self.jobs = SpriteGroup()

        for index, task_id in enumerate(TaskManager.get_current_tasks()):
            task = TaskManager.get_task(task_id)
            Text((140, 42 + (index * 35)), task.name, 16, Colors.SPRITE, self.jobs, centered=False)
            Text((140, 52 + (index * 35)), task.description, 16, Colors.SPRITE, self.jobs, centered=False)
            Text((140, 62 + (index * 35)), str(task.completed), 16, Colors.SPRITE, self.jobs, centered=False)

    def render(self) -> None:
        self.jobs.render(self.display)
