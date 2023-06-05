import pygame
from engine.scene.scene import Scene
from engine.objects.sprite import Sprite, SpriteGroup
from engine.assets import Assets
from engine.input import Input
from src.scenes.pause_menu.pause_objects import Tab
from src.scenes.pause_menu.inventory import Inventory
from src.scenes.pause_menu.jobs import Jobs
from src.scenes.pause_menu.map import Map
from src.scenes.pause_menu.glossary import Glossary
from src.scenes.pause_menu.options import Options
from src.scenes.pause_menu.exit import Exit
from engine.audio import AudioManager
from engine.window import Window


class Pause(Scene):
    def __init__(self, change_zone: callable = None, index=0):
        super().__init__("test")
        AudioManager.play_random_from("page_flip")
        self.categories = {"Inventario": Inventory(), "Trabajos": Jobs(), "Mapa": Map(change_zone),
                           "Opciones": Options(), "Salir": Exit()}
        self.book_background = Sprite((39, 16), Assets.images_book["book_background"], centered=False)
        self.tabs = [Tab((39, 50 + (index * 30)), name, self.interactive) for index, name in enumerate(self.categories)]
        self.selected_tab = self.tabs[index]
        self.selected_tab.set_state(self.selected_tab.State.SELECTED)
        self.bookmark = Sprite((95, 17), Assets.images_book[f"bookmark_{self.selected_tab.name}"], centered=False)
        self.x_padding = 8
        self.category_name: str = list(self.categories.keys())[index]

    @property
    def current_category(self) -> Scene:
        return self.categories[self.category_name]

    def update(self) -> None:
        self.current_category.update()
        for tab in self.tabs:
            tab.update()
            if tab.clicked and tab != self.selected_tab:
                AudioManager.play_random_from("page_flip")
                self.bookmark.image = Assets.images_book[f"bookmark_{tab.name}"]
                self.selected_tab.set_state(self.selected_tab.State.IDLE)
                self.selected_tab = tab
                self.selected_tab.set_state(self.selected_tab.State.SELECTED)
                self.category_name = tab.name.title()
        if Input.keyboard.keys["esc"]:
            from engine.scene.scene_manager import SceneManager
            from engine.preferences import Preferences
            Preferences.save()
            SceneManager.exit_scene()
        self.update_cursor()

    def render(self) -> None:
        from engine.scene.scene_manager import SceneManager
        self.display.blit(SceneManager.stack_scene[-2].display, (0, 0))
        self.book_background.render(self.display)
        self.bookmark.render(self.display)
        for tab in self.tabs:
            tab.render(self.display)

        self.current_category.render()
        self.display.blit(self.current_category.display, (0, 0))
