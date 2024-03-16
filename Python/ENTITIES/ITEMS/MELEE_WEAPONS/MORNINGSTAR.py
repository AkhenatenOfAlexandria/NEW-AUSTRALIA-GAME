from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class MORNINGSTAR(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=15):
        super().__init__((1, 8), "MORNINGSTAR", 4, POSITION, PRICE)
        