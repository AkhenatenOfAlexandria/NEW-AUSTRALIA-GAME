from ENTITIES.ENTITY import ENTITY
from WORLD.GLOBAL import ITEMS, ADD_ENTITY

class ITEM(ENTITY):

    def __init__(self, TYPE, POSITION, PRICE=0, *args, **kwargs):
        super().__init__(TYPE, POSITION, *args, **kwargs)
        
        ADD_ENTITY(self, ITEMS)
        self.ITEM_ID = ITEMS.index(self)
        self.NAME = f"{self.TYPE}.{self.ITEM_ID}"
        self.PRICE = PRICE
