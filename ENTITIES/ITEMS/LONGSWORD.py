from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON
from WORLD.GLOBAL_LISTS import ITEMS

class LONGSWORD(MELEE_WEAPON):

    def __init__(self, POSITION=None):
        super().__init__((1, 8), POSITION, "VERSATILE")

        self.NAME = f"LONGSWORD.{self.ITEM_ID}"