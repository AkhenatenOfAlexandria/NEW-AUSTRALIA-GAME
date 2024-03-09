from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class SPEAR(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=1):
        super().__init__((1, 6), "JAVELIN", POSITION, PRICE, "THROWN", "VERSATILE")
        