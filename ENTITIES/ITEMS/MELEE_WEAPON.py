from ENTITIES.ITEMS.ITEM import ITEM

class MELEE_WEAPON(ITEM):

    def __init__(self, DAMAGE, TYPE, POSITION=None, *args, **kwargs):
        super().__init__(TYPE, POSITION, *args, **kwargs)

        self.DAMAGE = DAMAGE
