from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class GLAIVE(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=20):
        super().__init__((1, 10), "GLAIVE", 6, POSITION, PRICE, None, "HEAVY", "REACH", "TWO-HANDED")
        