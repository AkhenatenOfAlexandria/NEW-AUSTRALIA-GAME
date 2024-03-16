from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY
from LOGIC.MATH import DISTANCE

import logging
import math

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class GIANT_LIZARD(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=15,
            DEXTERITY=12,
            CONSTITUTION=13,
            INTELLIGENCE=2,
            WISDOM=10,
            CHARISMA=5,
            HEALTH=19,
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
            "GIANT LIZARD",
            *args, **kwargs
            )
           
           self.CHARACTER = "L"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 50

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(3, 10) + 3
    
    
    def DEFAULT_ITEMS(self):
        pass
    

    def COMBAT_CHECK(self, ENEMY):
        DEATH = None
        GAME_RUNNING = True, True
        
        CHECK = ROLL(1, 20)
        if ENEMY.PRONE and DISTANCE(*self.POSITION[0:2], *ENEMY.POSITION[0:2]) < math.sqrt(2):
            CHECK = min(CHECK, ROLL(1,20))
        _CHECK = CHECK +4

        HUD = ""

        if CHECK == 1:
            logging.info(f"{self.NAME} attacked {ENEMY.NAME} and missed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and missed."
            
        elif CHECK == 20 or _CHECK > ENEMY.ARMOR_CLASS:

            if CHECK == 20:
                logging.info(f"CRITICAL HIT:")
                HUD += f"\nCRITICAL HIT: "
            else:
                HUD += "\n"
            DAMAGE = ROLL(1,8)+2
            ENEMY.HEALTH -= DAMAGE

            if ENEMY.HEALTH <= 0:
                DEATH = f"\n{ENEMY.NAME} died."
                
                GAME_RUNNING = ENEMY.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS
                
            logging.info(f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE.")
            HUD += f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE."
            if DEATH:
                HUD += DEATH

        else:
            logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and failed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and failed."
        
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

        return GAME_RUNNING
    