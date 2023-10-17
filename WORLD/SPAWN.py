import random

from ENTITIES.MOBS.KAREN import KAREN
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL
import WORLD.GAME_WORLD as _WORLD
from WORLD.GLOBAL_LISTS import PLAYERS, MOBS, REMOVE_ENTITY


def SPAWN(KAREN_COUNT):

    print("LOADING LEVEL...")
    for PLAYER in PLAYERS:
        PLAYER.POSITION = (0, 0)
        PLAYER.HEALTH = PLAYER.MAX_HEALTH

    for MOB in MOBS:
        if not MOB in PLAYERS:
            REMOVE_ENTITY(MOB)
    
    if KAREN_COUNT:
        print("ADDING MONSTERS...\n")
        for i in range(KAREN_COUNT):
            _LOCATION = None
            while not _LOCATION or _LOCATION == _WORLD.CENTRAL_ROOM:
                _POSITION = (random.randint(-15, 15), random.randint(-15, 15))
                _LOCATION = LOCATION_ID(*_POSITION) 
            _KAREN = KAREN(_POSITION, HEALTH=ROLL(2, 6))
    