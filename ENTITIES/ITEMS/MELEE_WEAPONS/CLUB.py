from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class CLUB(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=0.1):
        super().__init__((1, 4), "CLUB", POSITION, PRICE, "LIGHT")
        