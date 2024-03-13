from ENTITIES.ITEMS.ITEM import ITEM

class ARMOR(ITEM):

    def __init__(self, ARMOR_CLASS, TYPE, HEAVY=False, POSITION=None, PRICE=0, *args, **kwargs):
        super().__init__(TYPE, POSITION, PRICE, *args, **kwargs)

        self.ARMOR_CLASS = ARMOR_CLASS
        self.HEAVY = HEAVY
