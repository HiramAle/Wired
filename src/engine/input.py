import sys

import pygame.event

import src.engine.window as window
from src.constants.locals import CANVAS_WIDTH, CANVAS_HEIGHT
from src.constants.paths import BINDINGS, DEFAULT_BINDINGS
from src.utils.load import read_json, write_json


class Keyboard:
    """
    Keyboard input handler.
    """

    def __init__(self):
        """
        Initializes a new Keyboard object. Get the bindings from the JSON input preferences file, and set all it's
        bindings to False.

        """
        self.data = read_json(BINDINGS)
        self.keys = {key: False for key in self.data}
        self.key_pressed = ""


    def press_reset(self):
        """
        Resets the state of all keys to not pressed and keyPressed to empty.
        """
        for action in self.data:
            if self.data[action]["trigger"] == "press":
                self.keys[action] = False
        # self.keys = {key: False for key in self.keys if self.data[key]["trigger"] == "press"}
        self.key_pressed = ""

    def restore_bindings(self):
        """
        Loads the default key bindings.
        """
        self.data = read_json(DEFAULT_BINDINGS)

    # TODO: Adjust change and save bindings
    def change_binding(self, key: str, new_binding: int):
        """
        Changes the keycode of a given key.
        :param key: The key to change the binding of.
        :param new_binding: The new keycode for the key.
        """
        self.bindings[key] = new_binding

    def save_bindings(self):
        """
        Saves the current key bindings to a JSON file.
        """
        write_json(BINDINGS, self.bindings)

    def update(self, event: pygame.Event):
        """
        Updates the state of the keys based on the given Pygame event.
        :param event: The Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            for action in self.data:
                if event.key == self.data[action]["binding"]:
                    self.keys[action] = True

        if event.type == pygame.KEYUP:
            for action in self.data:
                if event.key == self.data[action]["binding"]:
                    self.keys[action] = False


class Mouse:
    """
    Mouse input handler.
    """

    def __init__(self):
        """
        Initializes a new Mouse object. Set the default button states and mouse position at 0,0.
        """
        self.buttons = {"left": False,
                        "right": False,
                        "left_hold": False,
                        "right_hold": False,
                        "left_release": False,
                        "right_release": False,
                        "scroll_up": False,
                        "scroll_down": False}

        self._position = pygame.Vector2(0, 0)

    def reset(self):
        """
        Resets the state of mouse buttons and scroll wheel to False.
        """
        self.buttons['left'] = False
        self.buttons['right'] = False
        self.buttons['left_release'] = False
        self.buttons['right_release'] = False
        self.buttons['scroll_up'] = False
        self.buttons['scroll_down'] = False

    def update(self, event: pygame.Event):
        """
        Updates the state of the mouse buttons and position based on the given Pygame event.
        :param event: The Pygame event to process.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._position.x = int(mouse_x / window.width * CANVAS_WIDTH)
        self._position.y = int(mouse_y / window.height * CANVAS_HEIGHT)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.buttons['left'] = True
                self.buttons['left_hold'] = True
            if event.button == 3:
                self.buttons['right'] = True
                self.buttons['right_hold'] = True
            if event.button == 4:
                self.buttons['scroll_up'] = True
            if event.button == 5:
                self.buttons['scroll_down'] = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.buttons['left_release'] = True
                self.buttons['left_hold'] = False
            if event.button == 3:
                self.buttons['right_release'] = True
                self.buttons['right_hold'] = False

    @property
    def position(self) -> tuple[int | float, int | float]:
        """
        :return: The current mouse position as a tuple.
        """
        return self._position.x, self._position.y

    @property
    def x(self) -> int | float:
        """
        :return: The x-coordinate of the current mouse position.
        """
        return self._position.x

    @property
    def y(self) -> int | float:
        """
        :return: The y-coordinate of the current mouse position.
        """
        return self._position.y


# Keyboard and Mouse variables for handle inputs
keyboard = Keyboard()
mouse = Mouse()


def update() -> None:
    """
    Process all events in the Pygame event queue and player input.
    """

    mouse.reset()
    keyboard.press_reset()

    for event in pygame.event.get():
        event: pygame.Event

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        mouse.update(event)
        keyboard.update(event)
