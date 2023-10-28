from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.ATTACK_PLAYER import ATTACK_PLAYER
from ENTITIES.ITEMS.MELEE_WEAPONS.SCIMITAR import SCIMITAR
from ENTITIES.ITEMS.ARMOR.LEATHER_ARMOR import LEATHER_ARMOR


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
           
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 50

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        return ATTACK_PLAYER(self)
