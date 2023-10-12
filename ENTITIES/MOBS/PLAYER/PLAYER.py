from ENTITIES.ITEMS.LONGSWORD import LONGSWORD
from ENTITIES.ITEMS.CHAIN_MAIL import CHAIN_MAIL
from ENTITIES.ITEMS.HANDAXE import HANDAXE
from ENTITIES.MOBS.MOB import MOB
from LOGIC.PROCESS_COMMAND import PROCESS_COMMAND
import WORLD.GAME_WORLD as _WORLD
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION
from LOGIC.MATH import ROLL


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
            "DEFENSE",
            *args, **kwargs
            )
        
        self.NAME = "YOU"
        self.INVENTORY["WEAPON"] = LONGSWORD()
        self.INVENTORY["SHIELD"] = True
        self.INVENTORY["ARMOR"] = CHAIN_MAIL()
        self.INVENTORY["GOLD"] = 10.0
        self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

        self.EXPERIENCE = 0
        self.EXPERIENCE_LEVEL = 1

        if not self.ATTRIBUTES:
            self.ATTRIBUTES = set("DEFENSE")
        


    def XP_LEVEL(self):
        _POINTS = self.EXPERIENCE
        _LEVEL = self.EXPERIENCE_LEVEL
        _LEVELS = {
            1: 0,
            2: 300,
            3: 900,
            4: 2700,
            5: 6500,
            6: 14000,
            7: 23000,
            8: 34000,
            9: 48000,
            10: 64000,
            11: 85000,
            12: 100000,
            13: 120000,
            14: 140000,
            15: 165000,
            16: 195000,
            17: 225000,
            18: 265000,
            19: 305000,
            20: 355000}
        
        for key, value in _LEVELS.items():
            if _POINTS >= value:
                _LEVEL = key
                if _LEVEL > self.EXPERIENCE_LEVEL:
                    self.EXPERIENCE_LEVEL = _LEVEL
                    HP = max((ROLL(1, 10) + self.CONSTITUTION_MODIFIER), 1)
                    self.MAX_HEALTH += HP
            else:
                break
    
    def ROOM_CHECK(self, MOBS):
        for mob in MOBS:
            if LOCATION_ID(*mob.POSITION) == LOCATION_ID(*self.POSITION) and mob != self:
                return True
        return False


    def UPDATE(self, MOBS, TURN, *args, **kwargs):
        LEVEL_COMPLETE = False
        _TURN = TURN
        OLD_POSITION = self.POSITION
        GAME_RUNNING, self.POSITION = PROCESS_COMMAND(self, MOBS)
        NEW_LOCATION = LOCATION_ID(*self.POSITION)
        if not NEW_LOCATION:
            print(f"ERROR: {self.POSITION} undefined.")
        elif NEW_LOCATION != _WORLD.VICTORY and NEW_LOCATION != LOCATION_ID(*OLD_POSITION):
            print(f"You entered a {NEW_LOCATION.DESCRIPTION}.{NEW_LOCATION.DESCRIBE_LOCATION(self)}")
            for mob in MOBS:
                if mob != self and LOCATION_ID(*mob.POSITION) == LOCATION_ID(*MOBS[0].POSITION):
                    MOB_INDEX = MOBS.index(self)
                    X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(*MOBS[0].POSITION, *mob.POSITION)
                    print(f"\t{mob.NAME} (ID: {MOB_INDEX}, HEALTH: {mob.HEALTH}/{mob.MAX_HEALTH}): {X_DISTANCE} feet {X_DIRECTION}, {Y_DISTANCE} feet {Y_DIRECTION}.")
        elif NEW_LOCATION == _WORLD.VICTORY:
            print(f"\nLevel complete!\n")
            input(f"End of TURN {TURN}. ENTER to continue.\n")
            _TURN += 1
            LEVEL_COMPLETE = True
        return GAME_RUNNING, LEVEL_COMPLETE, _TURN
