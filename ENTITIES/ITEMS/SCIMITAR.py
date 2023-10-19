from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON

class SCIMITAR(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 6), "SCIMITAR", POSITION, "FINESSE")
        