from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class HANDAXE(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=5):
        super().__init__((1, 6), "HANDAXE", POSITION, PRICE, "THROWN")
        