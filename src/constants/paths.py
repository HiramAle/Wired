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
# DATA_FOLDER = get_game_data_folder()
USER_DATA = "data/user"
SAVES_FOLDER = join(USER_DATA, "saves")
PREFERENCES = join(USER_DATA, "preferences.json")
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
IMAGES_CHARACTER_CREATION = "assets/images/character_creation"
IMAGES_ACTORS = "assets/images/actor"
IMAGES_WORLD = "assets/images/world"
IMAGES_BOOK = "assets/images/book"
IMAGES_ROUTING = "assets/images/routing"
IMAGES_TUTORIALS = "assets/images/tutorial"
IMAGES_STORE = "assets/images/store"
NPC_SPRITE_SHEETS = "assets/npcs/sprite_sheet"
NPC_PORTRAITS = "assets/npcs/portraits"
NPC_DATA = "data/npcs"

# Scene Data
DATA_CABLES = "data/scenes/cables.json"
DATA_CHARACTER_CREATION_FRAMES = "data/character_creation/animation_frames_data.json"
SUBNETTING_EXERCISES = "data/scenes/subnetting"
ROUTING_EXERCISES = "data/scenes/routing"
TUTORIALS = "data/tutorials"
# Maps
MAPS = {"players_house": "data/maps/TMX/Casa_custom.tmx",
        "village": "data/maps/TMX/Village.tmx",
        "store": "data/maps/TMX/Tienda_prueba.tmx",
        "city": "data/maps/TMX/City.tmx",
        "reception": "data/maps/TMX/reception.tmx",
        "company": "data/maps/TMX/Company.tmx",
        "chenchos_house": "data/maps/TMX/NPCs_house.tmx",
        "hotel": "data/maps/TMX/Hotel.tmx",
        "school": "data/maps/TMX/Escuela.tmx",
        "hospital": "data/maps/TMX/Hospital.tmx",
        "city_store": "data/maps/TMX/City_Store.tmx",
        "music_store": "data/maps/TMX/music_store.tmx"}
TILED_HOUSE = "data/maps/TMX/Casa_custom.tmx"
VILLAGE = "data/maps/TMX/Village.tmx"
# Character creation
BODIES = "assets/character_creation/bodies"
EYES = "assets/character_creation/eyes"
HAIRSTYLES = "assets/character_creation/hairstyles"
OUTFITS = "assets/character_creation/outfits"
# Character creation data
BODY_COLORS = "data/character_creation/bodies_colors.json"
EYES_COLORS = "data/character_creation/eyes_colors.json"
HAIRSTYLE_COLORS = "data/character_creation/hairstyles_colors.json"
OUTFIT_COLORS = "data/character_creation/outfits_colors.json"
