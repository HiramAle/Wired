from pygame import Surface
from engine.time import Time
from engine.animation.frame import Frame


class Animation:
    def __init__(self, sprite_sheet: Surface, data: dict):
        self.data = data
        self.sprite_sheet = sprite_sheet
        self.frames: list[Frame] = []
        for frame_data in data["frames"].values():
            self.frames.append(Frame(sprite_sheet, frame_data))
        self.__frame_index = 0
        self.time = 0
        self.is_playing = True
        self.loop = True
        self.length = sum(frame.duration for frame in self.frames)
        self.done = False

    def copy(self) -> "Animation":
        return Animation(self.sprite_sheet, self.data)

    def invert_order(self):
        self.frames: list[Frame] = []
        for frame_data in reversed(self.data["frames"].values()):
            self.frames.append(Frame(self.sprite_sheet, frame_data))

    def stop(self):
        if not self.is_playing:
            return
        self.is_playing = False

    def play(self):
        if self.is_playing:
            return
        self.is_playing = True

    def rewind(self):
        self.__frame_index = 0
        self.done = False

    def update(self):
        if not self.is_playing:
            return
        self.time += Time.dt * 1000
        if self.time < self.current_frame.duration:
            return
        self.__frame_index += 1
        self.time = 0
        if self.__frame_index >= len(self.frames):
            if self.loop:
                self.__frame_index = 0
            else:
                self.__frame_index = len(self.frames) - 1
                self.done = True
                self.is_playing = False

    @property
    def current_frame(self) -> Frame:
        return self.frames[self.__frame_index]
