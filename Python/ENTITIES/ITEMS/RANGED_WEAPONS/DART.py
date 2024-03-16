from ENTITIES.ITEMS.RANGED_WEAPONS.RANGED_WEAPON import RANGED_WEAPON

class DART(RANGED_WEAPON):

    def __init__(self, POSITION=None, PRICE=0.05):
        super().__init__((1, 4), "DART", (4, 12), 0.25, POSITION, PRICE, "FINESSE", "THROWN")
        