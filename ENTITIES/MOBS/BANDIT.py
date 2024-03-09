from ENTITIES.MOBS.ABORIGINE import ABORIGINE
from LOGIC.MATH import ROLL
from ENTITIES.ITEMS.MELEE_WEAPONS.SCIMITAR import SCIMITAR
from ENTITIES.ITEMS.ARMOR.LEATHER_ARMOR import LEATHER_ARMOR

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class BANDIT(ABORIGINE):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=11,
            DEXTERITY=12,
            CONSTITUTION=12,
            INTELLIGENCE=10,
            WISDOM=10,
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
            "ABORIGINE BANDIT",
            2,
            *args, **kwargs
            )
           
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 25

   
    def HEALTH_ROLL():
        return ROLL(2, 8) + 2
    
    
    def DEFAULT_ITEMS(self):
        self.INVENTORY["WEAPON"] = SCIMITAR()
        self.INVENTORY["ARMOR"] = LEATHER_ARMOR()
    