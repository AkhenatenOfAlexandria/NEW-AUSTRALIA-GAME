import math

from ENTITIES.ENTITY import ENTITY
from WORLD.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL


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
            *args
            ):
        super().__init__(POSITION)
        self.STRENGTH = STRENGTH
        self.DEXTERITY = DEXTERITY 
        self.CONSTITUTION = CONSTITUTION
        self.INTELLIGENCE = INTELLIGENCE
        self.WISDOM = WISDOM
        self.CHARISMA = CHARISMA
        self.STRENGTH_MODIFIER = math.floor((STRENGTH-10)/2)
        self.DEXTERITY_MODIFIER = math.floor((DEXTERITY-10)/2)
        self.CONSTITUTION_MODIFIER = math.floor((CONSTITUTION-10)/2)
        self.MAX_HEALTH = HEALTH + self.CONSTITUTION_MODIFIER
        self.HEALTH = self.MAX_HEALTH
        self.ARMOR_CLASS = self.DEXTERITY_MODIFIER + 10
        self.WEAPON = None
        for arg in args:
            setattr(self, arg, True)
    

    def COMBAT_CHECK(self, ENEMY, MOBS):
        ATTACK, GAME_RUNNING = False, True
        ATTACK = True
        CHECK = ROLL(1, 20)
        if CHECK == 1:
            input(f"{self.NAME} attacked {ENEMY.NAME} and missed.")
            return ATTACK, GAME_RUNNING
        elif CHECK == 20 or (CHECK+2) > ENEMY.ARMOR_CLASS:
            DAMAGE = max(0, self.STRENGTH_MODIFIER) + 3
            ENEMY.HEALTH -= DAMAGE
            if ENEMY.HEALTH <= 0:
                print(f"{self.NAME} hit {ENEMY.NAME}.")
                GAME_RUNNING = ENEMY.DIE(MOBS)
            else:
                input(f"{self.NAME} hit {ENEMY.NAME} (HEALTH: {ENEMY.HEALTH}/{ENEMY.MAX_HEALTH}).")
        else:
            input(f"{self.NAME} attacked {ENEMY.NAME} and missed.")

        return ATTACK, GAME_RUNNING
    
    
    def DIE(self, MOBS):
        MOBS.remove(self)
        input(f"{self.NAME} died.")
        if self.NAME == "YOU":
            return False
        else:
            return True
    
    
    def MOVE(self, DIRECTION, DISTANCE=1):
        X, Y = self.POSITION

        if DIRECTION == "NORTH":
            X -= DISTANCE
        elif DIRECTION == "SOUTH":
            X += DISTANCE
        elif DIRECTION == "EAST":
            Y += DISTANCE
        elif DIRECTION == "WEST":
            Y -= DISTANCE

        CURRENT_LOCATION = LOCATION_ID(*self.POSITION)
        NEW_LOCATION = LOCATION_ID(X, Y)
        
        if not CURRENT_LOCATION or NEW_LOCATION == CURRENT_LOCATION:
            return X, Y # Move the mob if he is clipped out of the map, but not if he would clip out of the map 
        elif DIRECTION in CURRENT_LOCATION.DOORS:
            DOOR_X, DOOR_Y = CURRENT_LOCATION.DOORS[DIRECTION]
            if (DIRECTION in ["NORTH", "SOUTH"] and DOOR_Y == Y) or (DIRECTION in ["EAST", "WEST"] and DOOR_X == X):
                return X, Y # Move the mob out of the room if he is aligned with the door

        return self.POSITION  # Keep the mob in the current position
