from WORLD.GLOBAL import PLAYERS
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL

import logging

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
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        X = CONSOLE.width//2 + self.POSITION[0] - PLAYER.POSITION[0]
        Y = CONSOLE.height//2 - self.POSITION[1] + PLAYER.POSITION[1]
        _CHARACTER = self.CHARACTER
        CONSOLE.print(X, Y, _CHARACTER)


    def MOVE(self, DIRECTION):
        X = self.POSITION[0]
        Y = self.POSITION[1]
        OLD_POSITION = X, Y
        if self.GRAPPLER:
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
