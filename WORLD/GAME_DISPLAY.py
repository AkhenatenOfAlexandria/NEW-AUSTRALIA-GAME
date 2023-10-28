from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION
from WORLD.GLOBAL import MOBS, GLOBAL_FLAGS, DISPLAY, UPDATE_DISPLAY, CLEAR_DISPLAY
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def MOB_INFO(PLAYER, MOB):
    X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(*PLAYER.POSITION[0:2], *MOB.POSITION[0:2])
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
    global GLOBAL_FLAGS, DISPLAY
    LEVEL, REALM = GLOBAL_FLAGS["LEVEL"], GLOBAL_FLAGS["REALM"]
    DEBUG = GLOBAL_FLAGS["DEBUG"]
    _INDEX = PLAYER.MOB_ID-1

    # MOB_NAMES = []
    for MOB in MOBS:
        '''if MOB:
            MOB_NAMES.append(MOB.NAME)
        else:
            MOB_NAMES.append(MOB)'''
        if MOB == PLAYER:
            if DEBUG:
                logging.debug(f"{LEVEL}, {REALM}")
            _COORDINATES = PLAYER.POSITION
            CURRENT_LOCATION = LOCATION_ID(*PLAYER.POSITION[0:2])
            _HEALTH = f"\nHEALTH: {PLAYER.HEALTH}/{PLAYER.MAX_HEALTH}."
            _ARMOR_CLASS = f"ARMOR CLASS: {PLAYER.ARMOR_CLASS}"
            _POSITION = f"LOCATION: {_COORDINATES}"
            UPDATE_DISPLAY("HEALTH", _INDEX, _HEALTH)
            UPDATE_DISPLAY("ARMOR CLASS", _INDEX, _ARMOR_CLASS)
            UPDATE_DISPLAY("POSITION", _INDEX, PLAYER.POSITION)
            CLEAR_DISPLAY("LOCATION", _INDEX)
            _LOCATION = f"{PLAYER.NAME} is in a {CURRENT_LOCATION.DESCRIPTION}.{CURRENT_LOCATION.DESCRIBE_LOCATION(PLAYER)}"
            UPDATE_DISPLAY("LOCATION", _INDEX, _LOCATION, APPEND=True)
            for i in [_HEALTH, _ARMOR_CLASS, PLAYER.POSITION]:
                print(i)
        elif MOB and LOCATION_ID(*MOB.POSITION[0:2]) == LOCATION_ID(*PLAYER.POSITION[0:2]):
            _MOB_INFO = MOB_INFO(PLAYER, MOB)
            UPDATE_DISPLAY("LOCATION", _INDEX, _MOB_INFO, APPEND=True)
    for i in DISPLAY["LOCATION"][_INDEX]:
        print(i)
    if DEBUG:
        logging.debug(len(MOBS))
