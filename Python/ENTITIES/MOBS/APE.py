from ENTITIES.MOBS.MOB import MOB
from ENTITIES.MOBS.AI.FOLLOW_PLAYER import ATTACK_PLAYER
from LOGIC.MATH import ROLL
from WORLD.GLOBAL import UPDATE_DISPLAY, DISPLAY

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class APE(MOB):
    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=16,
            DEXTERITY=14,
            CONSTITUTION=14,
            INTELLIGENCE=6,
            WISDOM=12,
            CHARISMA=7,
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
            "APE",
            *args, **kwargs
            )
           
           self.CHARACTER = "A"
           self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

           self.EXPERIENCE_POINTS = 100

           self.SPEED = 6
    

    def UPDATE(self, *args, **kwargs):
        ATTACK_PLAYER(self)

    
    def HEALTH_ROLL():
        return ROLL(1, 6)
    
    def DEFAULT_ITEMS(self):
        pass
    

    def COMBAT_CHECK(self, ENEMY):
        self.SEEN = True
        for i in range(2):
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
                DAMAGE = (
                    ROLL(1, 6) + 3
                )
                ENEMY.HEALTH -= DAMAGE

                if ENEMY.HEALTH <= 0:
                    DEATH = f"\n{ENEMY.NAME} died."
                    
                    GAME_RUNNING = ENEMY.DIE()
                    if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(ENEMY, 'EXPERIENCE_POINTS'):
                        self.EXPERIENCE += ENEMY.EXPERIENCE_POINTS
                    
                logging.info(f"{self.NAME} hit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE.")
                HUD += f"{self.NAME} hit {ENEMY.NAME}, dealing {DAMAGE} DAMAGE."
                if DEATH:
                    HUD += DEATH

            else:
                logging.debug(f"{self.NAME} attacked {ENEMY.NAME} and failed.")
                HUD += f"\n{self.NAME} attacked {ENEMY.NAME} and failed."
            
            UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

            return GAME_RUNNING
    