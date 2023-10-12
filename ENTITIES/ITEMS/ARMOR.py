from ENTITIES.ENTITY import ENTITY

class ARMOR(ENTITY):

    def __init__(self, ARMOR_CLASS, HEAVY=False, POSITION=None, *args, **kwargs):
        super().__init__(POSITION, *args, **kwargs)

        self.ARMOR_CLASS = ARMOR_CLASS
        self.HEAVY = HEAVY
