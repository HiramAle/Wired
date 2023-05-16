from src.scenes.world.zone import Zone


class ZoneManager:
    current_zone: Zone
    next_zone: Zone

    @classmethod
    def change_zone(cls, name: str):
        cls.next_zone = Zone(name, cls.current_zone.npc_list, cls.current_zone.player)

    @classmethod
    def update(cls):
        cls.current_zone.update()

    @classmethod
    def render(cls):
        cls.render()
