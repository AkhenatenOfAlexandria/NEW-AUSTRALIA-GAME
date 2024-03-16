from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY

import logging
import math

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class GIANT_CONSTRICTOR_SNAKE(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=19,
            DEXTERITY=14,
            CONSTITUTION=12,
            INTELLIGENCE=1,
            WISDOM=10,
            CHARISMA=3,
            HEALTH=13,
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
            "CONSTRICTOR SNAKE",
            *args, **kwargs
            )
           
           self.CHARACTER = "S"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 450

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        if self.GRAPPLED:
            pass
        else:
            ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(2, 10) + 2
    

    def GRAPPLE_CHECK(self):
        return 14
    
    
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
            DAMAGE = ROLL(2,8)+4
            
            ENEMY.HEALTH -= DAMAGE

            self.GRAPPLED = ENEMY
            ENEMY.GRAPPLER = self

            _HUD = f"{self.NAME} grappled {ENEMY.NAME}, dealing {DAMAGE} DAMAGE."
            logging.info(_HUD)
            HUD += _HUD
            if ENEMY.HEALTH <= 0:
                DEATH = f"\n{ENEMY.NAME} died."
                
                GAME_RUNNING = ENEMY.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS
            if DEATH:
                HUD += DEATH

        else:
            logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and failed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and failed."
        
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

        return GAME_RUNNING
    