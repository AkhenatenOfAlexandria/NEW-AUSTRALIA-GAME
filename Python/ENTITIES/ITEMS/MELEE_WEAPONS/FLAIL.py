from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class FLAIL(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=10):
        super().__init__((1, 8), "FLAIL", 2, POSITION, PRICE)
        