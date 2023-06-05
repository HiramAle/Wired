from engine.objects.sprite import Sprite
from engine.assets import Assets


class KeyHint(Sprite):
    class Type:
        TALK = "talk"
        SKIP = "skip"
        PAUSE = "pause"
        INTERACT = "interact"
        ENTER = "enter"
        SLEEP = "sleep"

    def __init__(self, hint_type: "Type"):
        super().__init__((541, 344), Assets.images_misc[f"{hint_type}_hint"])
        self._hint_type = hint_type
        self.pivot = self.Pivot.TOP_LEFT

    @property
    def hint_type(self) -> Type:
        return self._hint_type

    @hint_type.setter
    def hint_type(self, value: Type):
        self._hint_type = value
        self.image = Assets.images_misc[f"{value}_hint"]
