from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON

class HANDAXE(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 6), POSITION, "THROWN")

        self.NAME = "HANDAXE"