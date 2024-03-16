from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class WHIP(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=2):
        super().__init__((1, 4), "WHIP", 3, POSITION, PRICE, None, "FINESSE", "REACH")
        