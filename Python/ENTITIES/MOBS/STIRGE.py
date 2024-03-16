from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import BLOOD_DRAIN
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class STIRGE(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=16,
            DEXTERITY=11,
            CONSTITUTION=2,
            INTELLIGENCE=8,
            WISDOM=6,
            CHARISMA=4,
            HEALTH=2,
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
            "STIRGE",
            *args, **kwargs
            )
           
           self.CHARACTER = "B"
           self.ARMOR_CLASS = 14

           self.EXPERIENCE_POINTS = 25

           self.SPEED = 8

    def UPDATE(self, *args, **kwargs):
        BLOOD_DRAIN(self, self.ATTACHEE)

    
    def HEALTH_ROLL():
        return ROLL(1, 4)
    
    
    def DEFAULT_ITEMS(self):
        pass
    

    def COMBAT_CHECK(self, ENEMY):
        DEATH = None
        GAME_RUNNING = True, True
        
        CHECK = ROLL(1, 20)
        _CHECK = CHECK + 5

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
            DAMAGE = ROLL(1, 4) + 3
            ENEMY.HEALTH -= DAMAGE

            self.ATTACHEE = ENEMY
            ENEMY.ATTACHED = self

            logging.info(f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE.")
            HUD += f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE."

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
    