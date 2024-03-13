from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class DAGGER(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=2):
        super().__init__((1, 4), "DAGGER", POSITION, PRICE, "FINESSE", "LIGHT", "THROWN")
        