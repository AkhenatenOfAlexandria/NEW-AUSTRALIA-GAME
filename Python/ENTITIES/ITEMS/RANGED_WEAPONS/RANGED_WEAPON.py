from ENTITIES.ITEMS.ITEM import ITEM

class RANGED_WEAPON(ITEM):

    def __init__(self, DAMAGE, TYPE, RANGE, WEIGHT, POSITION=None, PRICE=0, *args, **kwargs):
        super().__init__(TYPE, POSITION, WEIGHT, PRICE, "RANGED", *args, **kwargs)
        
        self.DAMAGE = DAMAGE
        self.RANGE = RANGE
        self.DESCRIPTION = f"{self.NAME}: {self.PRICE} GOLD; {self.DAMAGE[0]}D{self.DAMAGE[1]} DAMAGE"
        self.SECOND_HAND = False
