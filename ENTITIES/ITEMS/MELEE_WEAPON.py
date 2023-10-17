from ENTITIES.ITEMS.ITEM import ITEM

class MELEE_WEAPON(ITEM):

    def __init__(self, DAMAGE, POSITION=None, *args, **kwargs):
        super().__init__(POSITION, *args, **kwargs)

        self.DAMAGE = DAMAGE
