from ENTITIES.ITEMS.ITEM import ITEM

class MELEE_WEAPON(ITEM):

    def __init__(self, DAMAGE, TYPE, POSITION=None, PRICE=0, *args, **kwargs):
        super().__init__(TYPE, POSITION, PRICE, *args, **kwargs)

        self.DAMAGE = DAMAGE