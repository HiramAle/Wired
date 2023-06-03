import pygame

from engine.assets import Assets
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, ItemSlot
from engine.task_manager import TaskManager
from engine.playerdata import PlayerData


class TaskLabel(Sprite):
    def __init__(self, position: tuple, task_id: str, *groups):
        super().__init__(position, Assets.images_book["task_title"], *groups)
        self.pivot = self.Pivot.TOP_LEFT
        self.task = TaskManager.get_task(task_id)
        self.task_title = Text(self.center, self.task.title, 16, Colors.SPRITE)

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        super().render(display)
        self.task_title.render(display)


class Jobs(Scene):
    def __init__(self):
        super().__init__("jobs")
        self.jobs = SpriteGroup()
        self.ui = SpriteGroup()

        Text((143 + 8, 42), "Trabajos", 32, Colors.SPRITE, self.ui, centered=False)
        
        for index, task in enumerate(PlayerData.tasks.current_tasks):
            TaskLabel((85 + 8, 90 + (index * 52)), task.id, self.jobs)
        self.task_title_frame = Sprite((346 + 8, 46), Assets.images_book["task_name"], self.ui, centered=False)
        self.task_title = Text(self.task_title_frame.center, "", 16, Colors.SPRITE, self.ui)
        self.task_description_frame = Sprite((351 + 8, 105), Assets.images_book["task_description"], self.ui,
                                             centered=False)
        self.task_description = Text(self.task_description_frame.center, "", 16, Colors.SPRITE, self.ui, max_width=160)

    def update(self) -> None:
        for job in self.jobs.sprites():
            job: TaskLabel
            if not job.hovered:
                continue
            self.task_title.text = job.task.title
            self.task_description.text = job.task.description

    def render(self) -> None:
        self.jobs.render(self.display)
        self.ui.render(self.display)
