from ENTITIES.MOBS.MOB import MOB
import ENTITIES.MOBS.AI.FOLLOW_PLAYER as FOLLOW_PLAYER
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import MELEE_RANGE
from ENTITIES.ITEMS.SCIMITAR import SCIMITAR
from ENTITIES.ITEMS.LEATHER_ARMOR import LEATHER_ARMOR
from WORLD.GLOBAL_LISTS import MOBS
from LOGIC.GLOBAL_FLAGS import GLOBAL_FLAGS


class KAREN(MOB):
    def __init__(
            self,
            POSITION=[0,0],
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
           
           self.INVENTORY["WEAPON"] = SCIMITAR()
           self.INVENTORY["SHIELD"] = True
           self.INVENTORY["ARMOR"] = LEATHER_ARMOR()
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 50

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        global GLOBAL_FLAGS
        TURN = GLOBAL_FLAGS["TURN"]
        GAME_RUNNING = True
        PLAYER = MOBS[0]
        DIRECTION = FOLLOW_PLAYER.DIRECTION(PLAYER, self)
        MOB_LOCATION = LOCATION_ID(*self.POSITION[0:2])
        PLAYER_LOCATION = LOCATION_ID(*PLAYER.POSITION[0:2])
        
        if MOB_LOCATION != PLAYER_LOCATION:
            pass

        elif MELEE_RANGE(*self.POSITION[0:2], *PLAYER.POSITION[0:2]):
            try:
                ATTACK, GAME_RUNNING = self.COMBAT_CHECK(PLAYER)
            except TypeError as e:
                print(f"TypeError: {e}.")
                GAME_RUNNING = False
        
        elif DIRECTION:
            # print(f"{self.NAME} attempting to move {DIRECTION}.")
            FOLLOW_PLAYER.MOVE(PLAYER, self, DIRECTION)

        return GAME_RUNNING, False