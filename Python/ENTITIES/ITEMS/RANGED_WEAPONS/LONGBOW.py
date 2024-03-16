from ENTITIES.ITEMS.RANGED_WEAPONS.RANGED_WEAPON import RANGED_WEAPON

class LONGBOW(RANGED_WEAPON):

    def __init__(self, POSITION=None, PRICE=50):
        super().__init__((1, 8), "LONGBOW", (30, 120), 2, POSITION, PRICE, "ARROWS", "TWO-HANDED", "HEAVY")
        