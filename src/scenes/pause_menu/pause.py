from engine.scene.scene import Scene
import engine.scene.scene_manager as scene_manager
import engine.input as game_input
from src.scenes.pause_menu.book import Book
from src.scenes.pause_menu.inventory_category import Inventory
from src.scenes.pause_menu.jobs_category import Jobs
from src.scenes.pause_menu.glossary_category import Glossary
from src.scenes.pause_menu.map_category import Map
from src.scenes.pause_menu.options_category import Options
from src.scenes.pause_menu.exit_category import Exit


class Pause(Scene):
    def __init__(self, index: int):
        super().__init__("pause")
        self.categories = [Inventory(), Jobs(), Glossary(), Map(), Options(), Exit()]
        self.book = Book(index, self.categories)

    def update(self) -> None:
        self.book.update()
        if game_input.keyboard.keys["esc"]:
            self.book.exiting = True

        if self.book.close:
            scene_manager.exit_scene()

    def render(self) -> None:
        self.display.blit(scene_manager.stack_scene[-2].display, (0, 0))
        self.book.render(self.display)
