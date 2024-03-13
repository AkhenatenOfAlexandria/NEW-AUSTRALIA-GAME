from WORLD.GAME_WORLD import GAME_WORLD
from WORLD.GLOBAL import GLOBAL_FLAGS

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def LOCATION_ID(X, Y):
        global GLOBAL_FLAGS
        LEVEL = GLOBAL_FLAGS["LEVEL"]
        COUNT = 0
        for GAME_LOCATION in GAME_WORLD[LEVEL]:
            COUNT += 1
            _MIN_X = GAME_LOCATION.MIN_X
            _MIN_Y = GAME_LOCATION.MIN_Y
            _MAX_X = GAME_LOCATION.MAX_X
            _MAX_Y = GAME_LOCATION.MAX_Y
            # logging.debug(f"{COUNT}. {GAME_LOCATION.DESCRIPTION}: {_MIN_X}, {_MIN_Y}, {_MAX_X}, {_MAX_Y}")
            if (
                GAME_LOCATION.MIN_X <= X <= GAME_LOCATION.MAX_X and
                GAME_LOCATION.MIN_Y <= Y <= GAME_LOCATION.MAX_Y
            ):
                return GAME_LOCATION
        return None
