from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION
from WORLD.GLOBAL_LISTS import MOBS, PLAYERS

def MOB_INFO(PLAYER, MOB):
    X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(*PLAYER.POSITION, *MOB.POSITION)
    _MOB_INFO = f"\t{MOB.NAME} (HP: {MOB.HEALTH}/{MOB.MAX_HEALTH}, AC: {MOB.ARMOR_CLASS}): {X_DISTANCE*5} feet {X_DIRECTION}, {Y_DISTANCE*5} feet {Y_DIRECTION}."

    INVENTORY = MOB.INVENTORY
    
    if INVENTORY["WEAPON"]:
        _MOB_INFO += f" Wielding {INVENTORY['WEAPON'].TYPE}"
        if INVENTORY["SHIELD"]:
            _MOB_INFO += " and SHIELD"
        _MOB_INFO += "."
    
    if INVENTORY["ARMOR"]:
        _MOB_INFO += f" Wearing {INVENTORY['ARMOR'].TYPE}."
    
    return _MOB_INFO


def GAME_DISPLAY(PLAYER):
    # MOB_NAMES = []
    for MOB in MOBS:
        '''if MOB:
            MOB_NAMES.append(MOB.NAME)
        else:
            MOB_NAMES.append(MOB)'''
        if MOB == PLAYER:
            CURRENT_LOCATION = LOCATION_ID(*MOB.POSITION)
            print(f"\nHEALTH: {MOB.HEALTH}/{MOB.MAX_HEALTH}.")
            print(f"ARMOR CLASS: {MOB.ARMOR_CLASS}")
            print(f"LOCATION: {MOB.POSITION}")
            print(f"{MOB.NAME} is in a {CURRENT_LOCATION.DESCRIPTION}.{CURRENT_LOCATION.DESCRIBE_LOCATION(MOB)}")
        elif MOB and LOCATION_ID(*MOB.POSITION) == LOCATION_ID(*MOBS[0].POSITION):
            # MOB_INDEX = MOBS.index(MOB)+1
            _MOB_INFO = MOB_INFO(PLAYER, MOB)
            print(_MOB_INFO)
    # print(len(MOBS), MOB_NAMES)
