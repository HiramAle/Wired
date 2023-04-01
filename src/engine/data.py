import pytmx
from src.utils.load import load_json
from src.constants.paths import DATA_CABLES, TILED_HOUSE

cable_data = {}
tiled_map = None


def init():
    global cable_data, tiled_map
    cable_data = load_json(DATA_CABLES)
    tiled_map = pytmx.load_pygame(TILED_HOUSE, pixelalpha=True)


