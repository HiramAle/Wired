from src.scenes.world.player import Player
from src.scenes.world.npc import NPC


class NPCManager:
    def __init__(self, player: Player):
        self.player = player
        self.npc_list = [NPC("kat", (0, 0), player)]
