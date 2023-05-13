from pygame import Surface, Rect, SRCALPHA


class Frame(Surface):
    def __init__(self, sprite_sheet: Surface, data: dict):
        x, y = data["frame"]["x"], data["frame"]["y"]
        self.width, self.height = data["frame"]["w"], data["frame"]["h"]
        super().__init__((self.width, self.height), SRCALPHA)
        self.blit(sprite_sheet, (0, 0), Rect(x, y, self.width, self.height))
        self.duration = data["duration"]

    def __repr__(self):
        return f"Frame({self.width}x{self.height}, {self.duration}ms)"
