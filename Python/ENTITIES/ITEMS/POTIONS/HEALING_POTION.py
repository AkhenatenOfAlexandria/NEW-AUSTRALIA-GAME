
from ENTITIES.ITEMS.ITEM import ITEM

class HEALING_POTION(ITEM):
    def __init__(self, POSITION=None, PRICE=50, *args, **kwargs):
        super().__init__("POTION-OF-HEALING", POSITION, 0.5, PRICE, *args, **kwargs)
