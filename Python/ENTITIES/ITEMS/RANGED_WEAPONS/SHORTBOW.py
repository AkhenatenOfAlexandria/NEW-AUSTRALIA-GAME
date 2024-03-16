from ENTITIES.ITEMS.RANGED_WEAPONS.RANGED_WEAPON import RANGED_WEAPON

class SHORTBOW(RANGED_WEAPON):

    def __init__(self, POSITION=None, PRICE=25):
        super().__init__((1, 6), "SHORTBOW", (16, 64), 2, POSITION, PRICE, "ARROWS", "TWO-HANDED")
        