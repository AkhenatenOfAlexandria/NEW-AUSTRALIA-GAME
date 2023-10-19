from ENTITIES.ENTITY import ENTITY
from WORLD.GLOBAL_LISTS import ITEMS, ADD_ENTITY

class ITEM(ENTITY):

    def __init__(self, TYPE, POSITION, *args, **kwargs):
        super().__init__(TYPE, POSITION, *args, **kwargs)
        
        ADD_ENTITY(self, ITEMS)
        self.ITEM_ID = ITEMS.index(self)
        self.NAME = f"{self.TYPE}.{self.ITEM_ID}"
