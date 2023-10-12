from WORLD.GAME_WORLD import GAME_WORLD

def LOCATION_ID(X, Y):
        for GAME_LOCATION in GAME_WORLD:
            if (
                GAME_LOCATION.MIN_X <= X <= GAME_LOCATION.MAX_X and
                GAME_LOCATION.MIN_Y <= Y <= GAME_LOCATION.MAX_Y
            ):
                return GAME_LOCATION
        return None
