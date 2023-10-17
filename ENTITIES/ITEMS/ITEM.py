from ENTITIES.ENTITY import ENTITY
from WORLD.GLOBAL_LISTS import ITEMS, ADD_ENTITY

class ITEM(ENTITY):

    def __init__(self, POSITION=None, *args, **kwargs):
        super().__init__(POSITION, *args, **kwargs)
        
        ADD_ENTITY(self, ITEMS)
        self.ITEM_ID = ITEMS.index(self)
