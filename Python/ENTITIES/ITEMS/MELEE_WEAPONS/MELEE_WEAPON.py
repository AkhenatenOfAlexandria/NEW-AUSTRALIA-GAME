from ENTITIES.ITEMS.ITEM import ITEM

class MELEE_WEAPON(ITEM):

    def __init__(self, DAMAGE, TYPE, WEIGHT, POSITION=None, PRICE=0, TWO_HANDED = None, *args, **kwargs):
        super().__init__(TYPE, POSITION, WEIGHT, PRICE, *args, **kwargs)
        
        self.DAMAGE1 = DAMAGE
        self.DAMAGE2 = TWO_HANDED
        self.DAMAGE = DAMAGE
        self.DESCRIPTION = f"{self.NAME}: {self.PRICE} GOLD"
        if self.DAMAGE2:
            self.DESCRIPTION += f"; (ONE-HANDED: {self.DAMAGE1[0]}D{self.DAMAGE1[1]} DAMAGE; TWO-HANDED: {self.DAMAGE2[0]}D{self.DAMAGE2[1]} DAMAGE)"
        else:
            self.DESCRIPTION += f"; {self.DAMAGE[0]}D{self.DAMAGE[1]} DAMAGE"
        self.SECOND_HAND = False
