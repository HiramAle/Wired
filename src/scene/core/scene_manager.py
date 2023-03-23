import pygame
from src.scene.core.scene import Scene
from src.scene.loading.loading import Loading
from src.scene.core.transition import CircularTransition
import src.engine.window as window

stack_scene: list[Scene] = []


def init():
    """
    Initializes the scene stack by setting the current scene to a Loading Scene.
    """
    set_scene(Loading())


def current_scene() -> Scene:
    """
    Returns the current scene on the top of the stack, if it exists.
    :return: The current scene on the top of the stack, or raises AssertionError if the stack is empty.
    """
    if not stack_scene:
        assert "Stack Scene is empty."
    return stack_scene[-1]


def set_scene(scene: Scene, swap=False):
    """
    Adds the specified scene to the top of the scene stack.
    :param scene: The scene to add to the stack.
    :param swap: If True, removes the current scene from the stack before adding the new scene. Defaults to False.
    """
    if swap:
        exit_scene()
    stack_scene.append(scene)
    scene.start()


def change_scene(from_scene: Scene, to_scene: Scene, transition=False, swap=False) -> None:
    """
    Changes the current scene from the specified 'from_scene' to the specified 'to_scene'.
    :param from_scene: The current scene to transition from.
    :param to_scene: The new scene to transition to.
    :param transition: If True, transitions between the scenes using a CircularTransition object. Defaults to False.
    :param swap: If True, removes the current scene from the stack before adding the new scene. Defaults to False.
    """
    if transition:
        set_scene(CircularTransition(from_scene, to_scene), swap)
    else:
        set_scene(to_scene, swap)


def exit_scene() -> None:
    """
    Removes the current scene from the top of the stack, if it exists.
    """
    if not stack_scene:
        return
    stack_scene.pop()


def update() -> None:
    """
    Calls the update method of the current scene on the top of the stack.
    """
    current_scene().update()


def render() -> None:
    """
    Calls the render method of the current scene on the top of the stack, and blits the resulting display to the window.
    """
    current_scene().render()
    window.screen.blit(pygame.transform.scale(current_scene().display, (window.width, window.height)), (0, 0))


def print_stack():
    """
    Prints the names of all scenes currently in the stack.
    """
    print([scene.name for scene in stack_scene])
