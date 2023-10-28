import random
import logging
import math

from ENTITIES.MOBS.KAREN import KAREN
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL
import WORLD.GAME_WORLD as _WORLD
from WORLD.GLOBAL import PLAYERS, MOBS, REMOVE_ENTITY, GLOBAL_FLAGS, CONTAINERS
from ENTITIES.ITEMS.CONTAINERS.CHEST import CHEST
from ENTITIES.ITEMS.ARMOR.LEATHER_ARMOR import LEATHER_ARMOR

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')




def SPAWN():
    global GLOBAL_FLAGS
    LEVEL, REALM, DEBUG = GLOBAL_FLAGS["LEVEL"], GLOBAL_FLAGS["REALM"], GLOBAL_FLAGS["DEBUG"]
    KAREN_COUNT = LEVEL

    print("LOADING LEVEL...")
    for PLAYER in PLAYERS:
        PLAYER.POSITION[2:4] = [LEVEL*2, REALM]
        PLAYER.XP_LEVEL()
        PLAYER.HEALTH = PLAYER.MAX_HEALTH

    for MOB in MOBS:
        if MOB and not MOB in PLAYERS:
            REMOVE_ENTITY(MOB)
    
    if KAREN_COUNT:
        for i in range(KAREN_COUNT):
            print(f"ADDING MONSTERS: {i+1}/{KAREN_COUNT}")
            _LOCATION = None
            while not _LOCATION or _LOCATION.START or _LOCATION.VICTORY:
                _POSITION = [random.randint(-256, 256), random.randint(-256, 256), LEVEL*2, REALM]
                _LOCATION = LOCATION_ID(*_POSITION[0:2]) 
            _KAREN = KAREN(_POSITION, HEALTH=ROLL(2, 6))
    
    print(f"ADDING CHESTS...")
    EMPTY_ROOMS = list(_WORLD.GAME_WORLD[LEVEL])
    
    CHEST_COUNT = 0
    while True:
        for ROOM in EMPTY_ROOMS:
            CHEST_SPAWN = random.randint(1, LEVEL)
            if CHEST_SPAWN == LEVEL and ROOM.DESCRIPTION == "SMALL ROOM" and not ROOM.VICTORY:
                CHEST_POSITION = (random.randint(ROOM.MIN_X, ROOM.MAX_X), random.randint(ROOM.MIN_Y, ROOM.MAX_Y), LEVEL, 0)
                ROOM.LOCAL_ITEMS.append(CHEST(CHEST_POSITION))
                EMPTY_ROOMS.remove(ROOM)
            CHEST_COUNT += 1
            print(f"{CHEST_COUNT}/{LEVEL*2}")
            if CHEST_COUNT >= LEVEL:
                break
        if CHEST_COUNT >= LEVEL:
                break
            
    
    CHEST_GOLD = LEVEL/10
    while CHEST_GOLD > 0:
        for container in CONTAINERS:
            if random.randint(1, len(CONTAINERS)) == 1:
                container.GOLD = round(container.GOLD+0.01, 2)
                CHEST_GOLD = round(CHEST_GOLD-0.01, 2)
                CHEST_COUNT = math.floor(LEVEL+CHEST_GOLD*10)
                print(f"{CHEST_COUNT}/{LEVEL*2}")


    if DEBUG:
            for ROOM in _WORLD.GAME_WORLD[LEVEL]:
                logging.debug(f"{ROOM.DESCRIPTION}:{ROOM.LOCAL_ITEMS}")
    
    if DEBUG:
        input()
