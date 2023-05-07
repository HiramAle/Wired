from src.scene.world.game_object import GameObject


class Position(GameObject):
    def __init__(self, name: str, position: tuple, properties: dict):
        super().__init__(position)
        self.name = name
        self.properties = properties

    @property
    def tuple(self):
        return self.position.x, self.position.y
