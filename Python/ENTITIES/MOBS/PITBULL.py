from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class PITBULL(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=13,
            DEXTERITY=14,
            CONSTITUTION=12,
            INTELLIGENCE=3,
            WISDOM=12,
            CHARISMA=7,
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
            "PITBULL",
            *args, **kwargs
            )
           
           self.CHARACTER = "D"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 25

           self.SPEED = 8
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(1, 8) + 1
    
    def DEFAULT_ITEMS(self):
        pass
    

    def COMBAT_CHECK(self, ENEMY):
        DEATH = None
        GAME_RUNNING = True, True
        
        CHECK = ROLL(1, 20)
        _CHECK = CHECK + 3

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
            DAMAGE = ROLL(1, 6) + 1
            ENEMY.HEALTH -= DAMAGE

            STRENGTH_SAVE = ROLL(1,20)
            if ENEMY.EXHAUSTION >= 3:
                STRENGTH_SAVE = min(STRENGTH_SAVE, ROLL(1,20))
            if ROLL (1, 20) + ENEMY.STRENGTH_MODIFIER < 11 and not ENEMY.PRONE:
                ENEMY.PRONE = True
                _PRONE = " and knocking him PRONE"
            else:
                _PRONE = ""

            if ENEMY.HEALTH <= 0:
                DEATH = f"\n{ENEMY.NAME} died."
                
                GAME_RUNNING = ENEMY.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS
                
            logging.info(f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE.")
            HUD += f"{self.NAME} bit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE{_PRONE}."
            if DEATH:
                HUD += DEATH

        else:
            logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and failed.")
            HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and failed."
        
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

        return GAME_RUNNING
    