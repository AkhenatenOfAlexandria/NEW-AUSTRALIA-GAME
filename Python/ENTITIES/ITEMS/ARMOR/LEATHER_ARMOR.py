from ENTITIES.ITEMS.ARMOR.ARMOR import ARMOR
from WORLD.GLOBAL import ITEMS

class LEATHER_ARMOR(ARMOR):

    def __init__(self, POSITION=None, PRICE=10, *args, **kwargs):
        super().__init__(11, "LEATHER ARMOR", 10, HEAVY=False, POSITION=POSITION, PRICE=PRICE, *args, **kwargs)
        