import pygame
from engine.time import Time


class AnimationData:
    def __init__(self, sprite_shet: pygame.Surface, data: dict):
        self.sprite_shet = sprite_shet
        self.frame_number = data.get("frames")
        self.speed = data.get("speed")
        self.width = data.get("width")
        self.height = data.get("height")
        self.looped = data.get("looped", True)


class Animation:
    """
    Component that represents that represent an animation made up of multiple frames.
    """

    def __init__(self, data: list):
        """
        Initializes a new Animation object.
        :param data: A list of Pygame Surfaces representing the frames of the animation.
        """
        self.data: dict = data[1]
        self.frames: list[pygame.Surface] = data[0]
        self._frame_index = 0
        self.speed = self.data["speed"]
        self.loop = True
        self.done = False

    def __repr__(self):
        return f"Animation({self.frames}, {self.data}, {self.speed}, {self.loop}, {self.done})"

    def rewind(self):
        self._frame_index = 0
        self.done = False

    def check_done(self):
        if self._frame_index >= len(self.frames) - 1:
            self.done = True
        else:
            self.done = False

    @property
    def frame(self) -> pygame.Surface:
        return self.frames[int(self._frame_index)]

    def play(self):
        """
        Plays the animation by incrementing the actual_frame attribute based on the speed and the delta time. If the
        actual_frame attribute exceeds the number of frames, it is reset to 0.
        """
        if not self.done:
            self._frame_index += self.speed * Time.dt
            if self._frame_index >= len(self.frames):
                if self.loop:
                    self._frame_index = 0
                else:
                    self.done = True
                    self._frame_index = len(self.frames) - 1
