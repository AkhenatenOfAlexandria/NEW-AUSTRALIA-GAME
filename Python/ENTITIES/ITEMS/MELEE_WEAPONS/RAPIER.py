from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class RAPIER(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=25):
        super().__init__((1, 8), "RAPIER", 2, POSITION, PRICE, None, "FINESSE")
