from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class GREATCLUB(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=0.2):
        super().__init__((1, 8), "GREATCLUB", 10, POSITION, PRICE, None, "TWO-HANDED")
