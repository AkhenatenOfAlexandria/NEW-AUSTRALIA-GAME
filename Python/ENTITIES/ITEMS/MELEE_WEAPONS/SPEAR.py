from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class SPEAR(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=1):
        super().__init__((1, 6), "SPEAR", 3, POSITION, PRICE, (1, 8), "THROWN", "VERSATILE")

        self.RANGE = (4, 12)
        