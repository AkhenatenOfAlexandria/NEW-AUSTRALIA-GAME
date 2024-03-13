from WORLD.LOCATIONS.LOCATION import LOCATION


class VICTORY(LOCATION):

    def __init__(self, X, Y, LEVEL, DOORS=None):
        super().__init__(X, Y, 6, 6, "VICTORY", LEVEL, DOORS=DOORS)
