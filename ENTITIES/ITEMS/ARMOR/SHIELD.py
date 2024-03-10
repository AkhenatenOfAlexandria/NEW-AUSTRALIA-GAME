from ENTITIES.ITEMS.ITEM import ITEM

class SHIELD(ITEM):

    def __init__(self, POSITION=None, PRICE=2, *args, **kwargs):
        super().__init__(TYPE="SHIELD", POSITION=POSITION, PRICE=PRICE, *args, **kwargs)
