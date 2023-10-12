from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import FOLLOW_PLAYER
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION
from ENTITIES.ITEMS.SCIMITAR import SCIMITAR
from ENTITIES.ITEMS.LEATHER_ARMOR import LEATHER_ARMOR


class KAREN(MOB):
    def __init__(
            self,
            POSITION,
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
            *args, **kwargs
            )
           self.NAME = "KAREN"
           self.INVENTORY["WEAPON"] = SCIMITAR()
           self.INVENTORY["SHIELD"] = True
           self.INVENTORY["ARMOR"] = LEATHER_ARMOR()
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 50
    

    def UPDATE(self, MOBS, TURN, *args, **kwargs):
        GAME_RUNNING = True
        PLAYER = MOBS[0]
        DIRECTION = FOLLOW_PLAYER(PLAYER, self)
        MOB_LOCATION = LOCATION_ID(*self.POSITION)
        PLAYER_LOCATION = LOCATION_ID(*PLAYER.POSITION)
        
        if MOB_LOCATION != PLAYER_LOCATION:
            pass

        elif DIRECTION:
            if MOB_LOCATION == PLAYER_LOCATION:
                START_IN_ROOM = True
            else:
                START_IN_ROOM = False
            NEW_POSITION = self.MOVE(DIRECTION)
            if NEW_POSITION != self.POSITION:
                self.POSITION = NEW_POSITION
                if LOCATION_ID(*self.POSITION) == LOCATION_ID(*PLAYER.POSITION):
                    if START_IN_ROOM:
                        print(f"{self.NAME} moved {DIRECTION}.")
                    else:
                        CURRENT_LOCATION = LOCATION_ID(*NEW_POSITION)
                        MOB_INDEX = MOBS.index(self)
                        X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(*PLAYER.POSITION, *self.POSITION)
                        print(f"{self.NAME} (ID: {MOB_INDEX}, HEALTH: {self.HEALTH}/{self.MAX_HEALTH}) entered the {CURRENT_LOCATION.DESCRIPTION}: {X_DISTANCE} feet {X_DIRECTION}, {Y_DISTANCE} feet {Y_DIRECTION}.")
        else:
            try:
                ATTACK, GAME_RUNNING = self.COMBAT_CHECK(PLAYER, MOBS)
            except TypeError as e:
                print(f"TypeError: {e}.")
                GAME_RUNNING = False
        return GAME_RUNNING, False, TURN