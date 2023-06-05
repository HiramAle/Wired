import pygame
from engine.loader import Loader
from engine.scene.scene import Scene
from engine.assets import Assets
from engine.objects.sprite import Sprite, SpriteGroup
from engine.ui.text import Text
from engine.ui.image import Image
from engine.input import Input
from engine.constants import Colors


class StepData:
    def __init__(self, data: dict):
        self.title = data["title"]
        self.description = data["description"]


class TutorialData:
    def __init__(self, name: str):
        data = Loader.load_json(f"data/tutorials/{name}.json")
        self.title = data["title"]
        self.steps = [StepData(step_data) for step_data in data["steps"]]


class Button(Sprite):
    def __init__(self):
        super().__init__((438, 288), Assets.images_tutorials["button_normal"])
        self.pivot = self.Pivot.TOP_LEFT
        self.outline_width = 3
        self.outline_color = Colors.GREEN

    def update(self, *args, **kwargs):
        if self.hovered and Input.mouse.buttons["left_hold"]:
            self.image = Assets.images_tutorials["button_pressed"]
        else:
            self.image = Assets.images_tutorials["button_normal"]

    def draw_outline(self, display: pygame.Surface):
        mask = pygame.mask.from_surface(self.image)
        surface = mask.to_surface(setcolor=self.outline_color, unsetcolor=(0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        rect = surface.get_rect(topleft=self.position)
        display.blit(surface, (rect.left + self.outline_width, rect.top))
        display.blit(surface, (rect.left - self.outline_width, rect.top))
        display.blit(surface, (rect.left, rect.top + self.outline_width))
        display.blit(surface, (rect.left, rect.top - self.outline_width))

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.hovered:
            self.draw_outline(display)
        super().render(display)


class Step(Sprite):
    def __init__(self, position: tuple, name: str, index: int):
        super().__init__(position, Loader.load_image(f"assets/tutorials/{name}/step{index}_icon.png"))
        self.pivot = self.Pivot.TOP_LEFT
        self.background = Sprite((self.x, self.y), pygame.Surface(self.image.get_size(), pygame.SRCALPHA))
        self.background.image.fill("#C1C0F3")
        self.background.opacity = 125
        self.background.pivot = self.background.Pivot.TOP_LEFT
        self.selected = True if index == 1 else False

    def render(self, display: pygame.Surface, offset=pygame.Vector2(0, 0)):
        if self.hovered or self.selected:
            self.background.render(display)
        super().render(display)


class Tutorial(Scene):
    def __init__(self, name: str):
        super().__init__("tutorial")
        self.module = name
        # ---------- Data ----------
        self.data = TutorialData(name)
        # ---------- Background ----------
        self.background = Sprite((27, 14), Assets.images_tutorials["tutorial_window"])
        self.background.pivot = self.background.Pivot.TOP_LEFT
        # ---------- Steps ----------
        self.steps: list[Step] = []
        self.step_images: list[Sprite] = []
        step_start_x = 44
        x = step_start_x
        y = 270

        number = 4 if name == "subnetting" else 5

        for index in range(number):
            self.steps.append(Step((x, y), name, index + 1))
            self.step_images.append(
                Sprite((237, 159.5), Assets.all_tutorials[name][f"tutorial_{index + 1}"]))
            x += 80
        self.__step_index = 0

        # ---------- Texts ----------
        self.texts = SpriteGroup()
        Text((45, 26), self.data.title, 32, Colors.SPRITE, self.texts, centered=False)
        self.step_title = Text((522, 44), self.data.steps[self.__step_index].title, 32, Colors.SPRITE, self.texts)
        self.step_desc = Text((447, 55), self.data.steps[self.__step_index].description, 16, Colors.SPRITE, self.texts,
                              max_width=152, centered=False)
        # ---------- Button ----------
        self.button = Button()

    @property
    def current_step(self) -> Step:
        return self.steps[self.__step_index]

    @current_step.setter
    def current_step(self, value: int):
        self.__step_index = value
        self.step_title.text = self.data.steps[self.__step_index].title
        self.step_desc.text = self.data.steps[self.__step_index].description

    def update(self) -> None:
        from engine.scene.scene_manager import SceneManager
        self.button.update()
        for index, step in enumerate(self.steps):
            if not step.clicked:
                continue
            self.current_step.selected = False
            self.current_step = index
            self.current_step.selected = True
            break

        if self.button.clicked:
            SceneManager.exit_scene()
            from engine.save_manager import instance as save_manager
            save_manager.active_save.tutorials[self.module] = True

    def render(self) -> None:
        from engine.scene.scene_manager import SceneManager
        self.display.blit(SceneManager.stack_scene[-2].display, (0, 0))
        self.background.render(self.display)
        for step in self.steps:
            step.render(self.display)
        self.texts.render(self.display)
        self.button.render(self.display)
        self.step_images[self.__step_index].render(self.display)
