import math

from ENTITIES.ENTITY import ENTITY
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL
from LOGIC.FUNCTIONS import INITIATIVE
from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY, MOBS, ADD_ENTITY, REMOVE_ENTITY
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


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
        DEATH = None
        GAME_RUNNING = True, True

        WEAPON = self.INVENTORY["WEAPON"]
        _PROFICIENCY = self.PROFICIENCY
        CHECK = ROLL(1, 20)
        _CHECK = CHECK + _PROFICIENCY

        HUD = ""
        
        if WEAPON and "FINESSE" in WEAPON.ATTRIBUTES:
            _CHECK += max(self.STRENGTH_MODIFIER, self.DEXTERITY_MODIFIER)
        else:
            _CHECK += self.STRENGTH_MODIFIER

        if CHECK == 1:
            logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and missed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and missed."
            
        elif CHECK == 20 or _CHECK > ENEMY.ARMOR_CLASS:

            if CHECK == 20:
                logging.debug(f"CRITICAL HIT:")
                HUD += f"\nCRITICAL HIT: "
            else:
                HUD += "\n"
            DAMAGE = (
                ROLL(*WEAPON.DAMAGE) + _PROFICIENCY if isinstance(WEAPON, MELEE_WEAPON)
                else max(0, self.STRENGTH_MODIFIER + _PROFICIENCY)
            )
            ENEMY.HEALTH -= DAMAGE

            if ENEMY.HEALTH <= 0:
                DEATH = f"\n{ENEMY.NAME} died."
                
                GAME_RUNNING = ENEMY.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS
                

            logging.debug(f"{self.NAME} hit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE.")
            HUD += f"{self.NAME} hit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE."
            if DEATH:
                HUD += DEATH

        else:
            logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and failed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and failed."
        
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

        return GAME_RUNNING
    
    
    def DIE(self):
        REMOVE_ENTITY(self)
        MESSAGE = f"{self.NAME} died."
        logging.debug(MESSAGE)

        return True
        

    def ROLL_INITIATIVE(self, *args):
        INITIATIVE_ROLL = ROLL(1, 20) + self.DEXTERITY_MODIFIER
        return INITIATIVE_ROLL