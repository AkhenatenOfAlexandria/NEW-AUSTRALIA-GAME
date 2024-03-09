from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from LOGIC.MATH import ROLL
from ENTITIES.ITEMS.MELEE_WEAPONS.CLUB import CLUB

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class ABORIGINE(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=10,
            DEXTERITY=10,
            CONSTITUTION=10,
            INTELLIGENCE=10,
            WISDOM=10,
            CHARISMA=10,
            HEALTH=4,
            NAME="ABORIGINE",
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
            NAME,
            2,
            *args, **kwargs
            )
           
           self.CHARACTER = "A"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 10

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(1, 8)
    
    
    def DEFAULT_ITEMS(self):
        self.INVENTORY["WEAPON"] = CLUB()
    