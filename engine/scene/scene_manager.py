import threading

import pygame
from engine.scene.scene import Scene
from src.scenes.loading.loading import Loading
from engine.scene.fade import FadeTransition
from src.scenes.main_menu.main_menu import MainMenu
from engine.assets import Assets
from engine.window import Window
from src.scenes.routing.routing import Routing
from src.scenes.cables.order import OrderCable
from src.scenes.subnetting.subnetting import Subnetting
from src.scenes.tutorial.tutorial import Tutorial
from src.scenes.store.store import Store
from src.scenes.world.sleep import Sleep


class SceneManager:
    stack_scene: list[Scene] = []
    scenes_by_name = {"cables": OrderCable,
                      "routing": Routing,
                      "subnetting": Subnetting,
                      "store": Store,
                      "sleep": Sleep}
    transitioning = False

    @classmethod
    def init(cls):
        """
        Initializes the scenes stack by setting the current scenes to a Loading Scene.
        """
        cls.set_active_scene(Loading(Assets.load, MainMenu))
        # cls.set_active_scene(Loading(Assets.load, Subnetting, None, ("reception",)))

    @classmethod
    def get_active_scene(cls) -> Scene:
        """
        Returns the current scene on the top of the stack, if it exists.
        :return: The current scene on the top of the stack, or raises AssertionError if the stack is empty.
        """
        if not cls.stack_scene:
            assert "Stack Scene is empty."
        return cls.stack_scene[-1]

    @classmethod
    def set_active_scene(cls, scene: Scene, swap=False):
        """
        Adds the specified scenes to the top of the scenes stack.
        :param scene: The scenes to add to the stack.
        :param swap: If True, removes the current scenes from the stack before adding the new scenes. Defaults to False.
        """
        if swap:
            cls.exit_scene()
        cls.stack_scene.append(scene)
        scene.start()

    @classmethod
    def change_scene(cls, to_scene: Scene, transition=False, swap=False, empty=False) -> None:
        """
        Changes the current scenes to the specified 'to_scene'.
        :param to_scene: The new scenes to transition to.
        :param transition: If True, transitions between the scenes using a CircularTransition object. Defaults to False.
        :param swap: If True, removes the current scenes from the stack before adding the new scenes. Defaults to False.
        :param empty: If True, removes the current scenes from the stack before adding the new scenes. Defaults to False.
        """
        if transition:
            cls.transitioning = True
            cls.set_active_scene(FadeTransition(cls.get_active_scene(), to_scene, empty), swap)
        else:
            cls.set_active_scene(to_scene, swap)

    @classmethod
    def exit_scene(cls) -> None:
        """
        Removes the current scenes from the top of the stack, if it exists.
        """
        if not cls.stack_scene:
            return
        cls.stack_scene.pop()

    @classmethod
    def update(cls) -> None:
        """
        Calls the update method of the current scenes on the top of the stack.
        """
        cls.get_active_scene().update()

    @classmethod
    def render(cls) -> None:
        """
        Calls the render method of the current scenes on the top of the stack, and blits the resulting display to the
        window.
        """
        cls.get_active_scene().render()
        Window.screen.blit(pygame.transform.scale(cls.get_active_scene().display, Window.size), (0, 0))

    @classmethod
    def print_stack(cls):
        """
        Prints the names of all scenes currently in the stack.
        """
        print([scene.name for scene in cls.stack_scene])

    @classmethod
    def clear(cls):
        cls.stack_scene = []
