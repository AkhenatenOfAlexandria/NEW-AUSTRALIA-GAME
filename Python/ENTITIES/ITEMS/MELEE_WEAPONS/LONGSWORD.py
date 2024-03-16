from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class LONGSWORD(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=15):
        super().__init__((1, 8), "LONGSWORD", 3, POSITION, PRICE, (1, 10), "VERSATILE")
        