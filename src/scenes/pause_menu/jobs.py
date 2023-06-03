import pygame

from engine.assets import Assets
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.constants import Colors
from engine.ui.text import Text
from src.scenes.pause_menu.pause_objects import PlayerAvatar, ItemSlot
from engine.task_manager import TaskManager
from engine.playerdata import PlayerData
from engine.ui.button import Button


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
        self.page_index = 0
        Text((143 + 8, 42), "Trabajos", 32, Colors.SPRITE, self.ui, centered=False)
        self.pages = []
        self.tasks = []
        # for index, task in enumerate(PlayerData.tasks.current_tasks):
        #     if index % 5 == 0 and index != 0:
        #         self.pages.append(self.tasks)
        #         self.tasks = []
        #     self.tasks.append(task)
        for index in range(0, len(PlayerData.tasks.current_tasks), 5):
            self.tasks = PlayerData.tasks.current_tasks[index:index + 5]
            self.pages.append(self.tasks)
        print(self.pages)
        self.render_tasks()
        self.task_title_frame = Sprite((346 + 8, 46), Assets.images_book["task_name"], self.ui, centered=False)
        self.task_title = Text(self.task_title_frame.center, "", 16, Colors.SPRITE, self.ui)
        self.task_description_frame = Sprite((351 + 8, 105), Assets.images_book["task_description"], self.ui,
                                             centered=False)
        self.task_description = Text(self.task_description_frame.center, "", 16, Colors.SPRITE, self.ui, max_width=160)
        self.left_button = Button((152, 297), Assets.images_book["button_left_normal"],
                                  Assets.images_book["button_left_pressed"], centered=False)
        self.right_button = Button((219, 297), Assets.images_book["button_right_normal"],
                                   Assets.images_book["button_right_pressed"], centered=False)

    @property
    def current_page(self) -> list:
        return self.pages[self.page_index]

    def update(self) -> None:
        self.left_button.update()
        self.right_button.update()
        for job in self.jobs.sprites():
            job: TaskLabel
            if not job.hovered:
                continue
            self.task_title.text = job.task.title
            self.task_description.text = job.task.description
        if self.left_button.clicked:
            self.page_index -= 1
            if self.page_index < 0:
                self.page_index = 0
            else:
                self.render_tasks()
        if self.right_button.clicked:
            self.page_index += 1
            if self.page_index >= len(self.pages):
                self.page_index = len(self.pages) - 1
            else:
                self.render_tasks()

    def render_tasks(self):
        self.jobs = SpriteGroup()
        for index, task in enumerate(self.current_page):
            TaskLabel((85 + 8, 80 + (index * 42)), task.id, self.jobs)

    def render(self) -> None:
        self.jobs.render(self.display)
        self.ui.render(self.display)
        self.left_button.render(self.display)
        self.right_button.render(self.display)
