import math

from ENTITIES.ENTITY import ENTITY
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL
from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON
from WORLD.GLOBAL_LISTS import PLAYERS, MOBS, INITIATIVE_MOBS, INITIATIVE_MOB_NAMES, ADD_ENTITY, REMOVE_ENTITY, INITIATIVE


class MOB(ENTITY):
    def __init__(
            self,
            POSITION,
            STRENGTH,
            DEXTERITY,
            CONSTITUTION,
            INTELLIGENCE,
            WISDOM,
            CHARISMA,
            HEALTH,
            TYPE,
            PROFICIENCY=0,
            *args, **kwargs
            ):
        super().__init__(TYPE, POSITION, *args, **kwargs)

        stats = {
            'STRENGTH': STRENGTH,
            'DEXTERITY': DEXTERITY,
            'CONSTITUTION': CONSTITUTION,
            'INTELLIGENCE': INTELLIGENCE,
            'WISDOM': WISDOM,
            'CHARISMA': CHARISMA
        }

        for stat, value in stats.items():
            setattr(self, f'{stat}', value)
            setattr(self, f'{stat}_MODIFIER', self.MODIFIER(value))

        ADD_ENTITY(self, MOBS)
        
        self.MOB_ID = MOBS.index(self)+1
        self.NAME = f"{self.TYPE}.{self.MOB_ID}"

        self.MAX_HEALTH = HEALTH + self.CONSTITUTION_MODIFIER
        self.HEALTH = self.MAX_HEALTH

        self.INVENTORY = {"WEAPON": None, "ARMOR": None, "SHIELD": False, "GOLD": 0.0, "ITEMS":[]}
        
        self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()
        self.PROFICIENCY = PROFICIENCY
    

    def MODIFIER(self, ATTRIBUTE):
        _MODIFIER = math.floor((ATTRIBUTE-10)/2)
        return _MODIFIER
    
    
    def ARMOR_CLASS_CALCULUS(self):
        _ARMOR = self.INVENTORY["ARMOR"]
        if _ARMOR:
            _ARMOR_CLASS = _ARMOR.ARMOR_CLASS
            if "DEFENSE" in self.ATTRIBUTES:
                _ARMOR_CLASS += 1
            if not _ARMOR.HEAVY:
                _ARMOR_CLASS += self.DEXTERITY_MODIFIER    

        else:
            _ARMOR_CLASS = 10 + self.DEXTERITY_MODIFIER
        
        if self.INVENTORY["SHIELD"]:
            _ARMOR_CLASS += 2


        
        return _ARMOR_CLASS
    
    
    def COMBAT_CHECK(self, ENEMY):
        ATTACK, GAME_RUNNING = True, True

        WEAPON = self.INVENTORY["WEAPON"]

        PROFICIENCY = 2

        CHECK = ROLL(1, 20)
        _CHECK = CHECK + PROFICIENCY
        
        if WEAPON and "FINESSE" in WEAPON.ATTRIBUTES:
            _CHECK += max(self.STRENGTH_MODIFIER, self.DEXTERITY_MODIFIER)
        else:
            _CHECK += self.STRENGTH_MODIFIER

        if CHECK == 1:
            print(f"{self.NAME} attacked {ENEMY.NAME} and missed.")
            
        elif CHECK == 20 or _CHECK > ENEMY.ARMOR_CLASS:

            if CHECK == 20:
                print(f"CRITICAL HIT:")
            DAMAGE = (
                ROLL(*WEAPON.DAMAGE) + PROFICIENCY if isinstance(WEAPON, MELEE_WEAPON)
                else max(0, self.STRENGTH_MODIFIER + PROFICIENCY)
            )
            ENEMY.HEALTH -= DAMAGE

            if ENEMY.HEALTH <= 0:
                print(f"{self.NAME} hit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE.")
                GAME_RUNNING = ENEMY.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS

            else:
                print(f"{self.NAME} hit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE (HEALTH: {ENEMY.HEALTH}/{ENEMY.MAX_HEALTH}).")

        else:
            print(f"{self.NAME} attacked {ENEMY.NAME} and failed.")

        return ATTACK, GAME_RUNNING
    
    
    def DIE(self):
        REMOVE_ENTITY(self)
        print(f"{self.NAME} died.")
        return True
    
    
    def MOVE(self, DIRECTION, DISTANCE=1):
        X, Y = self.POSITION
        MOVED = 0
        while MOVED < DISTANCE:
            if DIRECTION == "NORTH":
                X -= 1
            elif DIRECTION == "SOUTH":
                X += 1
            elif DIRECTION == "EAST":
                Y += 1
            elif DIRECTION == "WEST":
                Y -= 1
            MOVED +=1
            CURRENT_LOCATION = LOCATION_ID(*self.POSITION)
            NEW_LOCATION = LOCATION_ID(X, Y)
            # print(f"{self.NAME} MOVED {MOVED}/{DISTANCE}")

            if self in PLAYERS and CURRENT_LOCATION != NEW_LOCATION:
                INITIATIVE(self, NEW_LOCATION)
                break

            
        if not CURRENT_LOCATION or NEW_LOCATION == CURRENT_LOCATION:
            return X, Y # Move the mob if he is clipped out of the map, but not if he would clip out of the map 
        elif DIRECTION in CURRENT_LOCATION.DOORS:
            DOOR_X, DOOR_Y = CURRENT_LOCATION.DOORS[DIRECTION]
            if (DIRECTION in ["NORTH", "SOUTH"] and DOOR_Y == Y) or (DIRECTION in ["EAST", "WEST"] and DOOR_X == X):
                return X, Y # Move the mob out of the room if he is aligned with the door

        return self.POSITION  # Keep the mob in the current position

    def ROLL_INITIATIVE(self, *args):
        INITIATIVE_ROLL = ROLL(1, 20) + self.DEXTERITY_MODIFIER
        return INITIATIVE_ROLL