from engine.loader import Loader
from ctypes import windll
from engine.constants import Paths


class Preferences:
    filename = Paths.USER_PREFERENCES
    window_width = 0
    window_height = 0
    fullscreen = True
    borderless = False
    windowed = False
    volume = 4

    @classmethod
    def to_dict(cls) -> dict:
        return {
            "window_width": cls.window_width,
            "window_height": cls.window_height,
            "fullscreen": cls.fullscreen,
            "borderless": cls.borderless,
            "windowed": cls.windowed,
            "volume": cls.volume
        }

    @classmethod
    def load(cls):
        data = Loader.load_json(cls.filename)
        if data:
            cls.window_width = data["window_width"]
            cls.window_height = data["window_height"]
            cls.fullscreen = data["fullscreen"]
            cls.borderless = data["borderless"]
            cls.windowed = data["windowed"]
            cls.volume = data["volume"]
            print("Preferences loaded")
        else:
            print("Can't load preferences, writing new preferences file")
            user32 = windll.user32
            cls.window_width, cls.window_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            cls.save()

    @classmethod
    def save(cls):
        if Loader.save_json(cls.filename, cls.to_dict()):
            print("Preferences saved")
            return
        print("Can't load preferences")
