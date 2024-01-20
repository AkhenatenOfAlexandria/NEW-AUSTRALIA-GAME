import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Define the initial values for global variables in a dictionary
GLOBAL_FLAGS = {
    "DEBUG": True,
    "TIME": 0,
    "COMBAT": False,
    "LEVEL": 0,
    "REALM": 0,
    "NEW LEVEL": False
}

DISPLAY = {
    "HUD" : None,
    "INFO" : "\n"
}

DEBUG = GLOBAL_FLAGS["DEBUG"]

# Initialize global lists as empty lists
PLAYERS = []
KARENS = []
MOBS = []
NPM_TYPES = [KARENS]
ITEMS = []
CONTAINERS = []
INITIATIVE_MOBS = []
INITIATIVE_MOB_NAMES = []
OBJECTS = []


# Create a dictionary to store your lists for easy access
LISTS = [PLAYERS, MOBS, ITEMS, CONTAINERS, INITIATIVE_MOBS, INITIATIVE_MOB_NAMES, OBJECTS]


def INITIALIZE_DISPLAY():
    for PLAYER in PLAYERS:
        for KEY in [DISPLAY["HEALTH"], DISPLAY["ARMOR CLASS"], DISPLAY["POSITION"]]:
            KEY.append(None)
        DISPLAY["LOCATION"].append([])
        if GLOBAL_FLAGS["DEBUG"]:
            logging.debug(f"{PLAYER.NAME} added to DISPLAY.")


def REFRESH_DISPLAY():
    DISPLAY["GAME"] = f"TIME: {GLOBAL_FLAGS['TIME']}\nLEVEL: {GLOBAL_FLAGS['LEVEL']}"
    return DISPLAY["GAME"]


def CLEAR_DISPLAY(KEY, INDEX):
    while len(DISPLAY[KEY][INDEX]) > 0:
        DISPLAY[KEY][INDEX].pop()
    if GLOBAL_FLAGS["DEBUG"]:
        logging.debug(f"Cleared {KEY} DISPLAY.")

# Function to update display
def UPDATE_DISPLAY(KEY, VALUE, APPEND=False):
    global DISPLAY
    if KEY == "HUD":
        DISPLAY[KEY] = VALUE
    elif KEY == "INFO":
        DISPLAY[KEY] = '\n'+VALUE
    _DEBUG = f"{KEY} UPDATED: {DISPLAY[KEY]}"
    RETURN = DISPLAY[KEY]
    if GLOBAL_FLAGS["DEBUG"]:
            logging.debug(_DEBUG)
    return RETURN


# Function to update global variables
def UPDATE_FLAG(FLAG, VALUE):
    global GLOBAL_FLAGS
    if FLAG in GLOBAL_FLAGS:
        GLOBAL_FLAGS[FLAG] = VALUE
    if GLOBAL_FLAGS["DEBUG"]:
        logging.debug(f"{FLAG} UPDATED: {GLOBAL_FLAGS[FLAG]}")
    return GLOBAL_FLAGS[FLAG]


def ADD_ENTITY(ENTITY, *args):
    for LIST in args:
        if LIST in LISTS:
            LIST.append(ENTITY)
            if GLOBAL_FLAGS["DEBUG"]:
                logging.debug(f"Added {ENTITY.TYPE} to {LIST}.")
        else:
            logging.error(f"ERROR: LIST does not exist.")

def REMOVE_ENTITY(ENTITY):
    for LIST in LISTS:
        if ENTITY in LIST:
            ID = LIST.index(ENTITY)
            LIST[ID] = None
            if DEBUG:
                logging.debug(f"Removed {ENTITY.NAME} from {LIST}.")
