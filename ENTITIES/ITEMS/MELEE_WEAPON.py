from ENTITIES.ENTITY import ENTITY

class MELEE_WEAPON(ENTITY):

    def __init__(self, DAMAGE, POSITION=None, *args, **kwargs):
        super().__init__(POSITION, *args, **kwargs)

        self.DAMAGE = DAMAGE
