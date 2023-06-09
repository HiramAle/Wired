import os
import threading
from engine.loader import Loader
import pytmx
import src.utils.load as load
from src.constants.paths import *
from src.scenes.subnetting.subnetting_objects import SubnettingExercise
from src.scenes.world.npc import NPC
from src.scenes.routing.exercise import Exercise


class Data:
    cable_data = {}
    # Maps data from Tiled
    maps: dict[str, pytmx.TiledMap | None] = {}
    npcs: dict[str, dict] = {}
    # Character creation
    character_creation_frames: dict[str, dict[str, int]] = {zone_name for zone_name in MAPS.keys()}
    body_colors: dict[int, tuple] = {}
    eyes_colors: dict[int, tuple] = {}
    hairstyle_colors: dict[str, dict[int, tuple]] = {}
    outfit_colors: dict[int, dict[int, tuple]] = {}
    subnetting: dict[str, SubnettingExercise] = {}
    routing: dict[str, Exercise] = {}
    active_save: int = 0
    tutorials: {str, dict} = {}
    obj_npcs: list[NPC] = []

    @classmethod
    def init(cls):
        cls.cable_data = load.load_json(DATA_CABLES)
        cls.character_creation_frames = load.load_json(DATA_CHARACTER_CREATION_FRAMES)
        cls.body_colors = {int(key): tuple(value) for key, value in load.load_json(BODY_COLORS).items()}
        cls.eyes_colors = {int(key): tuple(value) for key, value in load.load_json(EYES_COLORS).items()}

        cls.hairstyle_colors = cls.convert_dictionary(load.load_json(HAIRSTYLE_COLORS))
        cls.outfit_colors = cls.convert_dictionary(load.load_json(OUTFIT_COLORS))
        cls.load_subnetting_exercises()
        cls.load_routing_exercises()
        cls.tutorials = {file.split(".")[0]: Loader.load_json(f"{TUTORIALS}/{file}") for file in os.listdir(TUTORIALS)}

    @classmethod
    def load_subnetting_exercises(cls):
        for exercise_file in os.listdir(SUBNETTING_EXERCISES):
            exercise_data = Loader.load_json(f"{SUBNETTING_EXERCISES}/{exercise_file}")
            zone_id = exercise_file.split(".")[0]
            cls.subnetting[zone_id] = SubnettingExercise(zone_id, exercise_data)

    @classmethod
    def load_routing_exercises(cls):
        for exercise_file in os.listdir(ROUTING_EXERCISES):
            exercise_data = Loader.load_json(f"{ROUTING_EXERCISES}/{exercise_file}")
            zone_id = exercise_file.split(".")[0]
            cls.routing[zone_id] = Exercise(exercise_data)

    @classmethod
    def load_world(cls, event: threading.Event):
        cls.maps = {}
        cls.obj_npcs = []
        for map_name in MAPS.keys():
            cls.maps[map_name] = pytmx.load_pygame(MAPS[map_name], pixelalpha=True)
        cls.npcs = {file.split(".")[0]: Loader.load_json(f"{NPC_DATA}/{file}") for file in os.listdir(NPC_DATA)}
        for npc_name, npc_data in cls.npcs.items():
            cls.obj_npcs.append(NPC(npc_name))
        event.clear()

    @staticmethod
    def convert_dictionary(dictionary: dict):
        new_dictionary = {}
        for key, value in dictionary.items():
            if key.isnumeric():
                new_key = int(key)
            else:
                new_key = key
            new_value = {}
            for k, v in value.items():
                new_value[int(k)] = tuple(v)
            new_dictionary[new_key] = new_value
        return new_dictionary
