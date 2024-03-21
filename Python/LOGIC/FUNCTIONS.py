import logging
import math

from WORLD.GLOBAL import PLAYERS, MOBS, INITIATIVE_MOBS, INITIATIVE_MOB_NAMES, GLOBAL_FLAGS, REMOVE_ENTITY
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from ENTITIES.ITEMS.ARMOR.CHAIN_SHIRT import CHAIN_SHIRT
from ENTITIES.ITEMS.ARMOR.CHAIN_MAIL import CHAIN_MAIL
from ENTITIES.ITEMS.ARMOR.LEATHER_ARMOR import LEATHER_ARMOR
from ENTITIES.ITEMS.MELEE_WEAPONS.CLUB import CLUB
from ENTITIES.ITEMS.MELEE_WEAPONS.GREATCLUB import GREATCLUB
from ENTITIES.ITEMS.MELEE_WEAPONS.HANDAXE import HANDAXE
from ENTITIES.ITEMS.MELEE_WEAPONS.JAVELIN import JAVELIN
from ENTITIES.ITEMS.MELEE_WEAPONS.LONGSWORD import LONGSWORD
from ENTITIES.ITEMS.MELEE_WEAPONS.QUARTERSTAFF import QUARTERSTAFF
from ENTITIES.ITEMS.MELEE_WEAPONS.SCIMITAR import SCIMITAR
from ENTITIES.ITEMS.MELEE_WEAPONS.SHORTSWORD import SHORTSWORD
from ENTITIES.ITEMS.MELEE_WEAPONS.SPEAR import SPEAR
from ENTITIES.ITEMS.MELEE_WEAPONS.DAGGER import DAGGER
from ENTITIES.ITEMS.ARMOR.SHIELD import SHIELD
from ENTITIES.ITEMS.MELEE_WEAPONS.BATTLEAXE import BATTLEAXE
from ENTITIES.ITEMS.MELEE_WEAPONS.FLAIL import FLAIL
from ENTITIES.ITEMS.MELEE_WEAPONS.GREATAXE import GREATAXE
from ENTITIES.ITEMS.MELEE_WEAPONS.GREATSWORD import GREATSWORD
from ENTITIES.ITEMS.MELEE_WEAPONS.HALBERD import HALBERD
from ENTITIES.ITEMS.MELEE_WEAPONS.LIGHT_HAMMER import LIGHT_HAMMER
from ENTITIES.ITEMS.MELEE_WEAPONS.MACE import MACE
from ENTITIES.ITEMS.MELEE_WEAPONS.MAUL import MAUL
from ENTITIES.ITEMS.MELEE_WEAPONS.SICKLE import SICKLE
from ENTITIES.ITEMS.MELEE_WEAPONS.WHIP import WHIP
from ENTITIES.ITEMS.MELEE_WEAPONS.MORNINGSTAR import MORNINGSTAR
from ENTITIES.ITEMS.MELEE_WEAPONS.GLAIVE import GLAIVE
from ENTITIES.ITEMS.MELEE_WEAPONS.PIKE import PIKE
from ENTITIES.ITEMS.MELEE_WEAPONS.RAPIER import RAPIER
from ENTITIES.ITEMS.MELEE_WEAPONS.TRIDENT import TRIDENT
from ENTITIES.ITEMS.MELEE_WEAPONS.WAR_PICK import WAR_PICK
from ENTITIES.ITEMS.RANGED_WEAPONS.DART import DART
from ENTITIES.ITEMS.RANGED_WEAPONS.SLING import SLING
from ENTITIES.ITEMS.RANGED_WEAPONS.SHORTBOW import SHORTBOW
from ENTITIES.ITEMS.RANGED_WEAPONS.LONGBOW import LONGBOW
from ENTITIES.ITEMS.POTIONS.HEALING_POTION import HEALING_POTION

from LOGIC.MATH import SLOPE, DISTANCE, PASSED

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

LOOT = ["ARROWS", "SLING-PELLETS", "WATER", BATTLEAXE, CHAIN_MAIL, CHAIN_SHIRT, CLUB, DAGGER, DART,
        FLAIL, GLAIVE, GREATAXE, GREATCLUB, GREATSWORD, HALBERD, HANDAXE, HEALING_POTION, JAVELIN,
        LEATHER_ARMOR, LIGHT_HAMMER, LONGBOW, LONGSWORD, MACE, MAUL, MORNINGSTAR, PIKE, QUARTERSTAFF,
         RAPIER, SCIMITAR, SHIELD, SHORTBOW, SHORTSWORD, SICKLE, SLING, SPEAR, TRIDENT, WAR_PICK, WHIP]


def SORT_MOBS_MELEE(MOB, REACH = False):
    POSITION1 = MOB.POSITION[0:2]
    ROOM = LOCATION_ID(*POSITION1)
    SIGHT = []
    mobs = {}
    if REACH:
        RANGE = math.sqrt(8)
    else:
        RANGE = math.sqrt(2)
    for mob in MOBS:
        POSITION1 = MOB.POSITION[0:2]
        if mob and mob !=MOB and mob.SEEN and LOCATION_ID(*mob.POSITION[0:2]) == ROOM and DISTANCE(*POSITION1, *mob.POSITION[0:2]) <= RANGE:
            mobs[mob] = mob.POSITION[0]
    
    while len(mobs):
        POSITION = float('inf')
        for mob, _POSITION in mobs.items():
            if _POSITION == min(_POSITION, POSITION):
                _mob = mob
                POSITION = _POSITION
        SIGHT.append(_mob)
        logging.debug(f"{SIGHT.index(_mob)}, {POSITION}")
        del mobs[_mob]
    
    for mob in SIGHT:
        mobs[mob] = mob.POSITION[1]
        SIGHT.remove(mob)
        logging.debug(f"{mobs[mob]}")
    
    while len(mobs):
        POSITION = float('inf')
        for mob, _POSITION in mobs.items():
            if _POSITION == min(_POSITION, POSITION):
                _mob = mob
                POSITION = _POSITION
        SIGHT.append(_mob)
        # logging.debug(f"{SIGHT.index(_mob)}, {POSITION}")
        del mobs[_mob]

    return SIGHT


def SORT_MOBS(MOB):
    POSITION1 = MOB.POSITION[0:2]
    ROOM = LOCATION_ID(*POSITION1)
    SIGHT = []
    mobs = {}
    for mob in MOBS:
        POSITION1 = MOB.POSITION[0:2]
        if mob and mob !=MOB and mob.SEEN and LOCATION_ID(*mob.POSITION[0:2]) == ROOM:
            mobs[mob] = DISTANCE(*mob.POSITION[0:2], *POSITION1)
    
    while len(mobs):
        POSITION = float('inf')
        for mob, _DISTANCE in mobs.items():
            if _DISTANCE == min(_DISTANCE, POSITION):
                _mob = mob
                POSITION = _DISTANCE
        SIGHT.append(_mob)
        logging.debug(f"{SIGHT.index(_mob)}, {POSITION}")
        del mobs[_mob]
    return SIGHT


def SIGHT_CHECK(MOB):
    logging.debug("Initiating SIGHT CHECK.")
    POSITION1 = MOB.POSITION[0:2]
    ROOM = LOCATION_ID(*POSITION1)
    SIGHT = []
    mobs = {}
    logging.debug("Initiating For Loop.")
    for mob in MOBS:
        POSITION1 = MOB.POSITION[0:2]
        if mob and mob !=MOB and LOCATION_ID(*mob.POSITION[0:2]) == ROOM:
            logging.debug("Mob found.")
            POSITION2 = mob.POSITION[0:2]
            if POSITION1[0] == POSITION2[0]:
                _SLOPE = float('inf')
            else:
                _SLOPE = SLOPE(*POSITION1, *POSITION2)
            dX = 1
            dY = 1
            if _SLOPE == float('inf'):
                dX = 0
            elif _SLOPE > 1:
                dX = 1/_SLOPE
            elif _SLOPE < 1:
                dY = _SLOPE
            X1, Y1 = POSITION1
            X2, Y2 = POSITION2
            X, Y = False, False
            if X1 > X2:
                X = True
            if Y1 > Y2:
                Y = True

            while not PASSED(X1, Y1, X2, Y2, X, Y) and LOCATION_ID(X1, Y1) == ROOM:
                X1 += dX
                Y1 += dY
                logging.debug(f"Checking {X1}, {Y1}")
                sight = True
                for mob2 in MOBS:
                    if mob2 and mob2.POSITION[0:2] == (math.floor(X1), math.floor(Y1)):
                        mobs[mob2] = DISTANCE(*POSITION1, *mob2.POSITION[0:2])
                        sight = False
                        break
                if not sight:
                    break
                
    
    POSITION = float('inf')
    while len(mobs):
        for mob, position in mobs.items():
            if position == min(position, POSITION):
                _mob = mob
        SIGHT.append(_mob)
        mobs.remove(_mob)
    return SIGHT
            


def LOOT_TABLE():
    TABLE = {}
    for loot in LOOT:
        if loot == "ARROWS":
            TABLE[loot] = (1/0.525)
        elif loot == "SLING-PELLETS":
            TABLE[loot] = (1/0.021)
        elif loot == "WATER":
            TABLE[loot] = 1/0.225
        else:
            l = loot()
            TABLE[loot] = (1/l.PRICE)
            REMOVE_ENTITY(l, SAFE=False)
    TOTAL_WEIGHT = sum(TABLE.values())
    for loot in TABLE.keys():
        TABLE[loot] = TABLE[loot] / TOTAL_WEIGHT

    return TABLE


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


