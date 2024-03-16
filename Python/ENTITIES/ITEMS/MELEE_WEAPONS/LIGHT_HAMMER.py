from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class LIGHT_HAMMER(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=2):
        super().__init__((1, 4), "LIGHT HAMMER", 2, POSITION, PRICE, None, "LIGHT", "THROWN")
        