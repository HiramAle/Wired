import pygame
from src.scene.scene import Scene
from src.custom_scenes.loading import Loading
from src.scene.transition import CircleTransition
import src.engine.window as window

stack_scene: list[Scene] = []


def init():
    set_scene(Loading())


def current_scene() -> Scene:
    if not stack_scene:
        return
    return stack_scene[-1]


def set_scene(scene: Scene, swap=False):
    if swap:
        exit_scene()
    stack_scene.append(scene)


def change_scene(from_scene: Scene, to_scene: Scene, transition=False, swap=False) -> None:
    if transition:
        set_scene(CircleTransition(from_scene, to_scene), swap)
    else:
        set_scene(to_scene, swap)


def exit_scene() -> None:
    if not stack_scene:
        return
    stack_scene.pop()


def update() -> None:
    current_scene().update()


def render() -> None:
    current_scene().render()
    window.screen.blit(pygame.transform.scale(current_scene().display, (window.width, window.height)), (0, 0))


def print_stack():
    print([scene.name for scene in stack_scene])
