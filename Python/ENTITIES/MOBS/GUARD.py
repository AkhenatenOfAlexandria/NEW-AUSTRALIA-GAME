from ENTITIES.MOBS.ABORIGINE import ABORIGINE
from LOGIC.MATH import ROLL
from ENTITIES.ITEMS.MELEE_WEAPONS.SPEAR import SPEAR
from ENTITIES.ITEMS.ARMOR.CHAIN_SHIRT import CHAIN_SHIRT

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class GUARD(ABORIGINE):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=13,
            DEXTERITY=12,
            CONSTITUTION=12,
            INTELLIGENCE=10,
            WISDOM=11,
            CHARISMA=10,
            HEALTH=11,
            *args, **kwargs
            ):
           super().__init__(
            POSITION,
            STRENGTH,
            DEXTERITY,
            CONSTITUTION,
            INTELLIGENCE,
            WISDOM,
            CHARISMA,
            HEALTH,
            "ABORIGINE GUARD",
            2,
            *args, **kwargs
            )
           
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 25

   
    def HEALTH_ROLL():
        return ROLL(2, 8) + 2
    
    
    def DEFAULT_ITEMS(self):
        self.INVENTORY["WEAPON"] = SPEAR()
        self.INVENTORY["SHIELD"] = True
        self.INVENTORY["ARMOR"] = CHAIN_SHIRT()
    