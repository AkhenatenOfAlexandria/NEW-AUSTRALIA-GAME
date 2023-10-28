from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class SCIMITAR(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=25):
        super().__init__((1, 6), "SCIMITAR", POSITION, PRICE, "FINESSE")
        