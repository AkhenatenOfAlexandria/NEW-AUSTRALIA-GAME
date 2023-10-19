from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON

class SHORTSWORD(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 6), "SHORTSWORD", POSITION, "FINESSE")
