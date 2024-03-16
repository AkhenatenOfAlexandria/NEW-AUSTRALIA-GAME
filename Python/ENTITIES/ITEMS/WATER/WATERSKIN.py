from ENTITIES.ITEMS.ITEM import ITEM

class WATER(ITEM):

    def __init__(self, WEIGHT=5, POSITION=None, PRICE=0.2, *args, **kwargs):
        super().__init__("WATER-SKIN", POSITION, PRICE, *args, **kwargs)

        self.WATER = 4
