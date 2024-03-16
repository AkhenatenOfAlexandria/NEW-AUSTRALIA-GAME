from ENTITIES.ITEMS.ITEM import ITEM

class WATER(ITEM):

    def __init__(self, TYPE, WEIGHT, POSITION=None, PRICE=0, *args, **kwargs):
        super().__init__(TYPE, POSITION, PRICE, *args, **kwargs)
        
