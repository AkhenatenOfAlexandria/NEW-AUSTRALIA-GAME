from WORLD.LOCATIONS.LOCATION import LOCATION


class CORRIDOR(LOCATION):

    def __init__(self, X, Y, LONG, LEVEL, LOCAL_ITEMS=None, DOORS=None, VICTORY=False):
        if LONG == "X":
            LENGTH_X = 28
            LENGTH_Y = 6
        else:
            LENGTH_X = 6
            LENGTH_Y = 28
        super().__init__(X, Y, LENGTH_X, LENGTH_Y, "CORRIDOR", LEVEL, LOCAL_ITEMS=LOCAL_ITEMS, DOORS=DOORS, VICTORY=VICTORY)
