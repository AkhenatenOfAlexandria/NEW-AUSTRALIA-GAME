from WORLD.GAME_WORLD import GAME_WORLD

def LOCATION_ID(X, Z):
        for GAME_LOCATION in GAME_WORLD:
            if (
                GAME_LOCATION.MIN_X <= X <= GAME_LOCATION.MAX_X and
                GAME_LOCATION.MIN_Z <= Z <= GAME_LOCATION.MAX_Z
            ):
                return GAME_LOCATION
        return False
