from WORLD.GAME_WORLD import GAME_WORLD
from WORLD.GLOBAL import GLOBAL_FLAGS

def LOCATION_ID(X, Y):
        global GLOBAL_FLAGS
        LEVEL = GLOBAL_FLAGS["LEVEL"]
        for GAME_LOCATION in GAME_WORLD[LEVEL]:
            if (
                GAME_LOCATION.MIN_X <= X <= GAME_LOCATION.MAX_X and
                GAME_LOCATION.MIN_Y <= Y <= GAME_LOCATION.MAX_Y
            ):
                return GAME_LOCATION
        return None
