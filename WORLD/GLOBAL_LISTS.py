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

    '''_MOBS_DICT = {}
    
    for PLAYER in PLAYERS:
        _MOBS[PLAYER] = None
        _MOBS.append(PLAYER)
    for LIST in NPM_TYPES:
        _MOBS[LIST] = None
        for MOB in LIST:
            _MOBS.append(MOB)
    
    for key in _MOBS_DICT.keys():
        if key in PLAYERS:
            _MOBS_DICT[key] = key.ROLL_INITIATIVE()
        elif key in NPM_TYPES:
            _INITIATIVE = key[0].ROLL_INITIATIVE()
            for MOB in key:
                _MOBS_DICT[MOB] = _INITIATIVE
            _MOBS_DICT.pop(key, None)
    
    _INITIATIVE_MOBS = sorted(_MOBS, key=lambda mob: _MOBS_DICT[mob])'''

    for MOB in MOBS:
        if MOB and (LOCATION_ID(*MOB.POSITION) == LOCATION or MOB == PLAYER):
            _MOBS.append(MOB)
    
    _INITIATIVE_MOBS = sorted(_MOBS, key=lambda mob: mob.ROLL_INITIATIVE())

    INITIATIVE_MOBS.clear()
    INITIATIVE_MOB_NAMES.clear()

    for MOB in _INITIATIVE_MOBS:
        INITIATIVE_MOBS.append(MOB)
        INITIATIVE_MOB_NAMES.append(MOB.NAME)
    # print(INITIATIVE_MOB_NAMES)
    return INITIATIVE_MOBS
