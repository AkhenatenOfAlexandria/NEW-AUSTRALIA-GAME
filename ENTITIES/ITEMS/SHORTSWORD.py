from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON
from WORLD.GLOBAL_LISTS import ITEMS

class SHORTSWORD(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 6), POSITION, "FINESSE")

        self.NAME = f"SHORTSWORD.{self.ITEM_ID}"