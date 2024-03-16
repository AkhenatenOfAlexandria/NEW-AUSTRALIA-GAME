from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class MACE(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=5):
        super().__init__((1, 6), "MACE", 4, POSITION, PRICE)
        