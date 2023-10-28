import logging

from WORLD.GLOBAL import MOBS, INITIATIVE_MOBS, INITIATIVE_MOB_NAMES, GLOBAL_FLAGS
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def INITIATIVE(PLAYER, LOCATION):
    DEBUG = GLOBAL_FLAGS["DEBUG"]
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
    if DEBUG:
        logging.debug(INITIATIVE_MOB_NAMES)
    return INITIATIVE_MOBS
