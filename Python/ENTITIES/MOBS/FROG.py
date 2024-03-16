from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FLEE_PLAYER import FLEE_PLAYER
from LOGIC.MATH import ROLL

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class FROG(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=1,
            DEXTERITY=13,
            CONSTITUTION=8,
            INTELLIGENCE=1,
            WISDOM=8,
            CHARISMA=3,
            HEALTH=3,
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
            "FROG",
            *args, **kwargs
            )
           
           self.CHARACTER = "f"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 0

           self.SPEED = 4
    

    def UPDATE(self, *args, **kwargs):
        FLEE_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(1, 6)
    
    
    def DEFAULT_ITEMS(self):
        pass
    

    def COMBAT_CHECK(self, ENEMY):
        pass
