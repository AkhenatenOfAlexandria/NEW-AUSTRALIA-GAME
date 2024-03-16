from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class PIKE(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=5):
        super().__init__((1, 10), "PIKE", 18, POSITION, PRICE, (1, 8), "HEAVY", "REACH", "TWO-HANDED")
        