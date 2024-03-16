from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class SICKLE(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=1):
        super().__init__((1, 4), "SICKLE", 2, POSITION, PRICE, None, "LIGHT")
        