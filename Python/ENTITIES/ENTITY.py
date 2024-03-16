from WORLD.GLOBAL import PLAYERS, UPDATE_DISPLAY, DISPLAY
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL, DISTANCE

import logging
import math

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


class ENTITY:

    def __init__(self, TYPE, POSITION=None, *args, **kwargs):
        self.POSITION = POSITION
        self.ARMOR_CLASS = 1
        self.INVENTORY = {"ITEMS":[]}
        self.TYPE = TYPE
        self.ATTRIBUTES = set(args)
        self.ATTACHEE = None
        self.ATTACHED = None


    def DRAW(self, CONSOLE):
        # logging.debug(f"Attempting to draw {self.NAME}.")
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        X = CONSOLE.width//2 + self.POSITION[0] - PLAYER.POSITION[0]
        Y = CONSOLE.height//2 - self.POSITION[1] + PLAYER.POSITION[1]
        _CHARACTER = self.CHARACTER
        CONSOLE.print(X, Y, _CHARACTER)
        # logging.debug(f"{self.NAME} drawn as {_CHARACTER} at {X} {Y}.")


    def MOVE(self, DIRECTION):
        X = self.POSITION[0]
        Y = self.POSITION[1]
        OLD_POSITION = X, Y
        if self.GRAPPLER:
            CHECK = ROLL(1,20)
            if self.EXHAUSTION >= 1:
                CHECK = min(CHECK, ROLL(1,20))
            if ROLL(1,20) + max(self.STRENGTH_MODIFIER, self.DEXTERITY_MODIFIER) > self.GRAPPLER.GRAPPLE_CHECK():
                logging.info(f"{self.NAME} escaped {self.GRAPPLER.NAME}'s GRAPPLE.")
                self.GRAPPLER.GRAPPLED = None
                self.GRAPPLER = None
            else:
                logging.info(f"{self.NAME} could not escape {self.GRAPPLER.NAME}'s GRAPPLE.")

        else:
            _OLD_LOCATION = LOCATION_ID(X, Y)
            if DIRECTION == "LEFT":
                POSITION = [X-1, Y]
            elif DIRECTION == "RIGHT":
                POSITION = [X+1, Y]
            elif DIRECTION == "UP":
                POSITION = [X, Y+1]
            elif DIRECTION == "DOWN":
                POSITION = [X, Y-1]
            _NEW_LOCATION = LOCATION_ID(*POSITION)
            if _NEW_LOCATION:
                logging.debug(f"OLD LOCATION: {_OLD_LOCATION.DESCRIPTION}; NEW LOCATION: {_NEW_LOCATION.DESCRIPTION}")
                if _NEW_LOCATION != _OLD_LOCATION:
                    for DOOR in _OLD_LOCATION.DOORS.values():
                        if OLD_POSITION == DOOR or tuple(POSITION) == DOOR:
                            return POSITION
                        else:
                            logging.debug(f"DOOR: {DOOR}, OLD_POSITION: {OLD_POSITION}, NEW_POSITION: {tuple(POSITION)}")
                else:
                    return POSITION
            else:
                logging.error("New Location does not exist.")
        return OLD_POSITION


    def RANGED_ATTACK(self, TARGET):
        WEAPON = self.INVENTORY["WEAPON"]
        if not WEAPON:
            logging.error("NO WEAPON FOUND.")
            return
        if 'THROWN' in WEAPON.ATTRIBUTES:
            self.INVENTORY["WEAPON"] = None
        if "ARROWS" in WEAPON.ATTRIBUTES:
            ARROWS = self.INVENTORY["ARROWS"]
            if ARROWS:
                ARROWS -= 1
            else:
                logging.info(f"{self.NAME} has no ARROWS.")
                HUD = f"\nNO ARROWS available."
                UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)
                return
        if "SLING-PELLETS" in WEAPON.ATTRIBUTES:
            PELLETS = self.INVENTORY["SLING-PELLETS"]
            logging.debug(f"Sling-Pellets required. {PELLETS} available.")
            if PELLETS:
                PELLETS -= 1
                logging.debug(f"{PELLETS} remaining.")
            else:
                logging.info(f"{self.NAME} has no SLING PELLETS.")
                HUD = f"\nNO SLING PELLETS available."
                UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)
                return

        DEATH = None
        GAME_RUNNING = True, True
        
        _PROFICIENCY = self.PROFICIENCY

        _DISTANCE = DISTANCE(*self.POSITION[0:2], *TARGET.POSITION[0:2])
        
        _CHECK = ROLL(1,20)
        
        ADVANTAGE = 0
        if self.PRONE:
            ADVANTAGE -= 1
        if TARGET.PRONE and _DISTANCE > math.sqr(2):
            ADVANTAGE -= 1
        if _DISTANCE <= math.sqrt(2) and not TARGET.PRONE:
            ADVANTAGE -= 1
        if _DISTANCE > WEAPON.RANGE[0]:
            ADVANTAGE -= 1
        if self.EXHAUSTION >= 3:
            ADVANTAGE -= 1

        if ADVANTAGE < 0:
            _CHECK = min(_CHECK, ROLL(1,20))
        CHECK = _CHECK + _PROFICIENCY

        HUD = ""
        
        if "FINESSE" in WEAPON.ATTRIBUTES:
            CHECK += max(self.STRENGTH_MODIFIER, self.DEXTERITY_MODIFIER)
        else:
            CHECK += self.STRENGTH_MODIFIER

        if _CHECK == 1 or _DISTANCE > WEAPON.RANGE[1]:
            if 'THROWN' in WEAPON.ATTRIBUTES:
                if _CHECK == 1:
                    if TARGET.INVENTORY["WEAPON"]:
                        TARGET.INVENTORY["ITEMS"].append(WEAPON)
                    else:
                        TARGET.INVENTORY["WEAPON"] = WEAPON
                else:
                    WEAPON.POSITION = TARGET.POSITION[0:4]
                    ROOM = LOCATION_ID(*TARGET.POSITION[0:2])
                    ROOM.ADD_ITEM(WEAPON)
            logging.info(f"{self.NAME} attacked {TARGET.NAME} with {WEAPON.NAME} and missed.")
            HUD += f"\n{self.NAME} attacked {TARGET.NAME} with {WEAPON.NAME} and missed."
            
        elif _CHECK == 20 or CHECK > TARGET.ARMOR_CLASS:
            if 'THROWN' in WEAPON.ATTRIBUTES:
                WEAPON.POSITION = TARGET.POSITION[0:4]
                ROOM = LOCATION_ID(*TARGET.POSITION[0:2])
                ROOM.ADD_ITEM(WEAPON)
                WEAPON.ATTACHEE = TARGET
                TARGET.ATTACHED = WEAPON
            if _CHECK == 20:
                logging.info(f"CRITICAL HIT:")
                HUD += f"\nCRITICAL HIT: "
            else:
                HUD += "\n"
            DAMAGE = (
                ROLL(*WEAPON.DAMAGE) + _PROFICIENCY
            )
            
            TARGET.HEALTH -= DAMAGE

            if TARGET.HEALTH <= 0:
                DEATH = f"\n{TARGET.NAME} died."
                
                GAME_RUNNING = TARGET.DIE()
                if hasattr(self, 'EXPERIENCE_LEVEL') and hasattr(TARGET, 'EXPERIENCE_POINTS'):
                    self.EXPERIENCE += TARGET.EXPERIENCE_POINTS
                

            logging.info(f"{self.NAME} hit {TARGET.NAME} with {WEAPON.NAME}, dealing {DAMAGE} DAMAGE.")
            HUD += f"{self.NAME} hit {TARGET.NAME} with {WEAPON.NAME}, dealing {DAMAGE} DAMAGE."

            if DEATH:
                HUD += DEATH

        else:
            if 'THROWN' in WEAPON.ATTRIBUTES:
                WEAPON.POSITION = TARGET.POSITION[0:4]
                ROOM = LOCATION_ID(*TARGET.POSITION[0:2])
                ROOM.ADD_ITEM(WEAPON)
            logging.info(f"{self.NAME} attacked {TARGET.NAME} with {WEAPON.NAME} and failed.")
            HUD += f"\n{self.NAME} attacked {TARGET.NAME} with {WEAPON.NAME} and failed."
        
        UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+HUD)

        return GAME_RUNNING