from ENTITIES.ITEMS.ARMOR import ARMOR

class LEATHER_ARMOR(ARMOR):

    def __init__(self, POSITION=None, *args, **kwargs):
        super().__init__(ARMOR_CLASS=11, HEAVY=False, POSITION=POSITION, *args, **kwargs)

        self.NAME = "LEATHER ARMOR"
