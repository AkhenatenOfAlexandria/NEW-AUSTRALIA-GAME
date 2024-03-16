from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class QUARTERSTAFF(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=0.2):
        super().__init__((1, 6), "QUARTERSTAFF", 4, POSITION, PRICE, (1, 8), "VERSATILE")
        