from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON
from WORLD.GLOBAL_LISTS import ITEMS

class HANDAXE(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 6), "HANDAXE", POSITION, "THROWN")