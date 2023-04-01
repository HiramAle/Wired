from os.path import dirname, join, expanduser, exists
from os import makedirs
from src.constants.locals import GAME_NAME


def get_game_data_folder() -> str:
    """
    Check if the OneDrive sync it's active and locates the "My Games" folder.
    :return: "My Games" folder path.
    """
    # Possible paths
    local_games_folder = join(expanduser("~"), "Documents", "My Games")
    one_drive_folder = join(expanduser("~"), "OneDrive")
    es_onedrive_folder = join(expanduser("~"), "OneDrive", "Documentos")
    en_onedrive_folder = join(expanduser("~"), "OneDrive", "Documents")
    # Determine if OneDrive sync is active and the language of it
    onedrive_active = False
    onedrive_language = None
    if exists(one_drive_folder):
        onedrive_active = True
        onedrive_language = "spanish" if exists(es_onedrive_folder) else "english"
    # Set the default save folder and the game name
    save_folder = local_games_folder
    game_name = GAME_NAME
    # Set the save folder in case OneDrive sync is active
    if onedrive_active:
        if onedrive_language == "spanish":
            save_folder = join(es_onedrive_folder, "My Games", game_name)
        elif onedrive_language == "english":
            save_folder = join(en_onedrive_folder, "My Games", game_name)
    else:
        save_folder = join(save_folder, game_name)
    # If the directory doesn't exist, create it
    if not exists(save_folder):
        makedirs(save_folder)
    return save_folder


# Data paths
ROOT = dirname(dirname(__file__))
DATA_FOLDER = get_game_data_folder()
SAVES_FOLDER = join(DATA_FOLDER, "Saves")
PREFERENCES = join(DATA_FOLDER, "preferences.json")
SAVES = [join(SAVES_FOLDER, f"slot_{i}") for i in range(1, 4)]
DEFAULT_PREFERENCES = "data/default/preferences.json"
BINDINGS = "data/user/bindings.json"
DEFAULT_BINDINGS = "data/default/bindings.json"
# Assets
CURSORS = "assets/cursors"
FONTS = "assets/fonts"
IMAGES_MISC = "assets/images/misc"
ANIMATIONS = "assets/animations"
IMAGES_MAIN_MENU = "assets/images/main_menu"
IMAGES_SELECTOR = "assets/images/selector"
IMAGES_CABLES = "assets/images/cables"
IMAGES_SUBNETTING = "assets/images/subnetting"
# Scene Data
DATA_CABLES = "data/scenes/cables.json"
# Maps
TILED_HOUSE = "data/maps/TMX/Players_House.tmx"

