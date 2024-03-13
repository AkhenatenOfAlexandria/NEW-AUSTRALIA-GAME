from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from ENTITIES.ITEMS.MELEE_WEAPONS.DAGGER import DAGGER
from LOGIC.MATH import ROLL


class KOBOLD(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=7,
            DEXTERITY=15,
            CONSTITUTION=9,
            INTELLIGENCE=8,
            WISDOM=7,
            CHARISMA=8,
            HEALTH=5,
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
            "KOBOLD",
            2,
            *args, **kwargs
            )
           
           self.CHARACTER = "k"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 50

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(2, 6) - 2
    
    def DEFAULT_ITEMS(self):
        self.INVENTORY["WEAPON"] = DAGGER()
        