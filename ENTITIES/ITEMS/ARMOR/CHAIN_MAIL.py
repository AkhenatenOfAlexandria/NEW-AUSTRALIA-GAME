from ENTITIES.ITEMS.ARMOR.ARMOR import ARMOR
from WORLD.GLOBAL import ITEMS

class CHAIN_MAIL(ARMOR):

    def __init__(self, POSITION=None, PRICE=75, *args, **kwargs):
        super().__init__(16, "CHAIN MAIL", True, POSITION, PRICE, *args, **kwargs)