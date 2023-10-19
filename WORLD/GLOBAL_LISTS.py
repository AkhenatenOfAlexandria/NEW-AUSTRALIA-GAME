from WORLD.LOCATION_ID import LOCATION_ID

# Initialize global lists as empty lists
PLAYERS = []
KARENS = []
MOBS = []
NPM_TYPES = [KARENS]
ITEMS = []
INITIATIVE_MOBS = []
INITIATIVE_MOB_NAMES = []

# Create a dictionary to store your lists for easy access
LISTS = [PLAYERS, MOBS, ITEMS, INITIATIVE_MOBS, INITIATIVE_MOB_NAMES]


def ADD_ENTITY(ENTITY, *args):
    for LIST in args:
        if LIST in LISTS:
            LIST.append(ENTITY)
        else:
            print(f"ERROR: LIST does not exist.")

def REMOVE_ENTITY(ENTITY):
    for LIST in LISTS:
        if ENTITY in LIST:
            ID = LIST.index(ENTITY)
            LIST[ID] = None
            # print(f"Removed {ENTITY} from {LIST}.")

def INITIATIVE(PLAYER, LOCATION):
    
    _MOBS = []
    
    for MOB in MOBS:
        if MOB and (LOCATION_ID(*MOB.POSITION[0:2]) == LOCATION or MOB == PLAYER):
            _MOBS.append(MOB)
    
    _INITIATIVE_MOBS = sorted(_MOBS, key=lambda mob: mob.ROLL_INITIATIVE())

    INITIATIVE_MOBS.clear()
    INITIATIVE_MOB_NAMES.clear()

    for MOB in _INITIATIVE_MOBS:
        INITIATIVE_MOBS.append(MOB)
        INITIATIVE_MOB_NAMES.append(MOB.NAME)
    # print(INITIATIVE_MOB_NAMES)
    return INITIATIVE_MOBS
