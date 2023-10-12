from ENTITIES.MOBS.MOB import MOB
from LOGIC.PROCESS_COMMAND import PROCESS_COMMAND
import WORLD.GAME_WORLD as _WORLD
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION

class PLAYER(MOB):
    def __init__(
            self,
            POSITION=(0,0),
            STRENGTH=16,
            DEXTERITY=14,
            CONSTITUTION=15,
            INTELLIGENCE=13,
            WISDOM=11,
            CHARISMA=9,
            HEALTH=10,
            *args
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
            *args
            )
        
        self.NAME = "YOU"


    def UPDATE(self, MOBS, *args):
        OLD_POSITION = self.POSITION
        GAME_RUNNING, self.POSITION = PROCESS_COMMAND(self, MOBS)
        NEW_LOCATION = LOCATION_ID(*self.POSITION)
        if not NEW_LOCATION:
            print(f"ERROR: {self.POSITION} undefined.")
        elif NEW_LOCATION != _WORLD.VICTORY and NEW_LOCATION != LOCATION_ID(*OLD_POSITION):
            input(f"You entered a {NEW_LOCATION.DESCRIPTION}. {NEW_LOCATION.DESCRIBE_LOCATION(self)}")
            for mob in MOBS:
                if mob != self and LOCATION_ID(*mob.POSITION) == LOCATION_ID(*MOBS[0].POSITION):
                    MOB_INDEX = MOBS.index(self)
                    X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(*MOBS[0].POSITION, *mob.POSITION)
                    print(f"{mob.NAME} (ID: {MOB_INDEX}, HEALTH: {mob.HEALTH}/{mob.MAX_HEALTH}): {X_DISTANCE} feet {X_DIRECTION}, {Y_DISTANCE} feet {Y_DIRECTION}.")
        elif NEW_LOCATION == _WORLD.VICTORY:
            print(f"\nLevel complete!\n")
            GAME_RUNNING = False
        return GAME_RUNNING
