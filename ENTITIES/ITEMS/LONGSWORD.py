from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON

class LONGSWORD(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 8), "LONGSWORD", POSITION, "VERSATILE")
        