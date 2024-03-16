from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class TRIDENT(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=5):
        super().__init__((1, 6), "TRIDENT", 4, POSITION, PRICE, (1, 8), "THROWN", "VERSATILE")

        self.RANGE = (4, 12)
        