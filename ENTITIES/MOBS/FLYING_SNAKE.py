from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY

import logging
import math

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class FLYING_SNAKE(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=4,
            DEXTERITY=18,
            CONSTITUTION=11,
            INTELLIGENCE=2,
            WISDOM=12,
            CHARISMA=5,
            HEALTH=5,
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
            "FLYING SNAKE",
            *args, **kwargs
            )
           
           self.CHARACTER = "s"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 25

           self.SPEED = 12
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(2, 4)
    
    
    def DEFAULT_ITEMS(self):
        pass
    

    def COMBAT_CHECK(self, ENEMY):
        DEATH = None
        GAME_RUNNING = True, True
        
        CHECK = ROLL(1, 20)
        _CHECK = CHECK + 6

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
            DAMAGE = 1
            POISON_DAMAGE = ROLL(3, 4)

            ENEMY.HEALTH -= DAMAGE + POISON_DAMAGE

            if ENEMY.HEALTH <= 0:
                DEATH = f"\n{ENEMY.NAME} died."
                
                GAME_RUNNING = ENEMY.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS
                
            logging.info(f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE and {POISON_DAMAGE} POISON DAMAGE.")
            HUD += f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE and {POISON_DAMAGE} POISON DAMAGE."
            if DEATH:
                HUD += DEATH

        else:
            logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and failed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and failed."
        
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

        return GAME_RUNNING
    