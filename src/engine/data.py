from src.utils.load import read_json
from src.constants.paths import DATA_CABLES

cable_data = {}


def init():
    global cable_data
    cable_data = read_json(DATA_CABLES)
