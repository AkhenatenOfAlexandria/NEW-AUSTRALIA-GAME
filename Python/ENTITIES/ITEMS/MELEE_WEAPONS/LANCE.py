from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class LANCE(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=10):
        super().__init__((1, 12), "LANCE", 6, POSITION, PRICE, None, "REACH", "TWO-HANDED")
