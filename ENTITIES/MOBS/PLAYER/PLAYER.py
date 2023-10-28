from ENTITIES.ITEMS.MELEE_WEAPONS.LONGSWORD import LONGSWORD
from ENTITIES.ITEMS.ARMOR.CHAIN_MAIL import CHAIN_MAIL
from ENTITIES.ITEMS.MELEE_WEAPONS.HANDAXE import HANDAXE
from ENTITIES.MOBS.MOB import MOB
from LOGIC.PROCESS_COMMAND import PROCESS_COMMAND
import WORLD.GAME_WORLD as _WORLD
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import MOBS, PLAYERS, ADD_ENTITY
from WORLD.GAME_DISPLAY import GAME_DISPLAY, MOB_INFO
from WORLD.GLOBAL import GLOBAL_FLAGS, UPDATE_FLAG
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class PLAYER(MOB):

    def __init__(
            self,
            POSITION=[0,0,0,0],
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
            "PLAYER",
            2,
            "DEFENSE",
            *args, **kwargs
            )
        
        ADD_ENTITY(self, PLAYERS)

        self.NAME = f"PLAYER {self.MOB_ID}"

        self.INVENTORY["GOLD"] = 10.0

        self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

        self.EXPERIENCE = 0
        self.EXPERIENCE_LEVEL = 1

        self.SPEED = 6

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
    
    def ROOM_CHECK(self):
        for mob in MOBS:
            if mob and LOCATION_ID(*mob.POSITION[0:2]) == LOCATION_ID(*self.POSITION[0:2]) and mob != self:
                return True
        return False


    def UPDATE(self, *args, **kwargs):
        global GLOBAL_FLAGS
        TURN, COMBAT, DEBUG = GLOBAL_FLAGS["TURN"], GLOBAL_FLAGS["COMBAT"], GLOBAL_FLAGS["DEBUG"]
        

        GAME_DISPLAY(self)
        GAME_RUNNING = True
        LEVEL_COMPLETE = False
        ACTION = self.SPEED*5
        MOVEMENT = self.SPEED*5
        
        while (ACTION or MOVEMENT) and GAME_RUNNING and not LEVEL_COMPLETE:
            OLD_POSITION = self.POSITION
            OLD_LOCATION = LOCATION_ID(*OLD_POSITION[0:2])
            GAME_RUNNING, self.POSITION[0:2], ACTION, MOVEMENT = PROCESS_COMMAND(self, ACTION, MOVEMENT)
            NEW_LOCATION = LOCATION_ID(*self.POSITION[0:2])
            COMBAT = UPDATE_FLAG("COMBAT", self.ROOM_CHECK())
            
            if DEBUG:
                logging.debug(f"POSITION: {self.POSITION}; ACTION: {ACTION}; MOVEMENT: {MOVEMENT}; COMBAT: {COMBAT}")
            if not NEW_LOCATION:
                logging.error(f"ERROR: {self.POSITION} undefined.")
            elif not NEW_LOCATION.VICTORY and NEW_LOCATION != OLD_LOCATION:
                print(f"{self.NAME} entered a {NEW_LOCATION.DESCRIPTION}.{NEW_LOCATION.DESCRIBE_LOCATION(self)}")
                for mob in MOBS:
                    if mob and mob != self and LOCATION_ID(*mob.POSITION[0:2]) == LOCATION_ID(*self.POSITION[0:2]):
                        _MOB_INFO = MOB_INFO(self, mob)
                        print(_MOB_INFO)
                if COMBAT:
                    break
            elif NEW_LOCATION.VICTORY:
                print(f"\nLevel complete!\n")
                input(f"End of TURN {TURN}. ENTER to continue.\n")
                TURN = UPDATE_FLAG("TURN", TURN+1)
                LEVEL_COMPLETE = True
        return GAME_RUNNING, LEVEL_COMPLETE
    
    def DIE(self):
        if self not in PLAYERS:
            ADD_ENTITY(self, PLAYERS)
        print(f"{self.NAME} died.")
        return False
