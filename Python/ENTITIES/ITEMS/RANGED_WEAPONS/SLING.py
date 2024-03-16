from ENTITIES.ITEMS.RANGED_WEAPONS.RANGED_WEAPON import RANGED_WEAPON

class SLING(RANGED_WEAPON):

    def __init__(self, POSITION=None, PRICE=0.1):
        super().__init__((1, 4), "SLING", (6, 24), 0, POSITION, PRICE, "SLING-PELLETS")
        