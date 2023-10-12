from ENTITIES.ITEMS.ARMOR import ARMOR

class CHAIN_MAIL(ARMOR):

    def __init__(self, POSITION=None, *args, **kwargs):
        super().__init__(ARMOR_CLASS=16, HEAVY=True, POSITION=POSITION, *args, **kwargs)

        self.NAME = "CHAIN MAIL"
