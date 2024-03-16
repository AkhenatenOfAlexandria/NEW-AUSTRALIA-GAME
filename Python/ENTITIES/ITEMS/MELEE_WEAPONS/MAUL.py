from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class MAUL(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=10):
        super().__init__((2, 6), "MAUL", 10, POSITION, PRICE, None, "HEAVY", "TWO-HANDED")
        