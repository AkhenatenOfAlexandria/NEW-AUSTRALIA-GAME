from ENTITIES.ITEMS.ITEM import ITEM

class ARMOR(ITEM):

    def __init__(self, ARMOR_CLASS, TYPE, HEAVY=False, POSITION=None, *args, **kwargs):
        super().__init__(TYPE, POSITION, *args, **kwargs)

        self.ARMOR_CLASS = ARMOR_CLASS
        self.HEAVY = HEAVY
