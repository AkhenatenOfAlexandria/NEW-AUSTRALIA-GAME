from ENTITIES.ITEMS.ARMOR.ARMOR import ARMOR

class CHAIN_SHIRT(ARMOR):

    def __init__(self, POSITION=None, PRICE=50, *args, **kwargs):
        super().__init__(13, "CHAIN-SHIRT", 20, HEAVY="MEDIUM", POSITION=POSITION, PRICE=PRICE, *args, **kwargs)