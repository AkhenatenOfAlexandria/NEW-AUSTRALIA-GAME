from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from ENTITIES.ITEMS.MELEE_WEAPONS.SCIMITAR import SCIMITAR
from ENTITIES.ITEMS.ARMOR.LEATHER_ARMOR import LEATHER_ARMOR
from LOGIC.MATH import ROLL


class KAREN(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=8,
            DEXTERITY=14,
            CONSTITUTION=10,
            INTELLIGENCE=10,
            WISDOM=8,
            CHARISMA=8,
            HEALTH=7,
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
            "KAREN",
            2,
            *args, **kwargs
            )
           
           self.CHARACTER = "K"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 50

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(2, 6)
    
    def DEFAULT_ITEMS(self):
        self.INVENTORY["WEAPON"] = SCIMITAR()
        self.INVENTORY["ARMOR"] = LEATHER_ARMOR()
        self.INVENTORY["SHIELD"] = True
    