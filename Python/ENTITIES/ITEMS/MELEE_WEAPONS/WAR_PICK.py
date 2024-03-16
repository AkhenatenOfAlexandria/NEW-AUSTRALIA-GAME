from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON

class WAR_PICK(MELEE_WEAPON):

    def __init__(self, POSITION=None, PRICE=5):
        super().__init__((1, 8), "WAR PICK", 2, POSITION, PRICE)
        