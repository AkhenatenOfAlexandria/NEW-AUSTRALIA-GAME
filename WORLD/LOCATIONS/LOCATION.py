import logging

from LOGIC.MATH import RELATIVE_LOCATION
from WORLD.GLOBAL import GLOBAL_FLAGS

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

class LOCATION:

    def __init__(self, X, Y, LENGTH_X, LENGTH_Y, DESCRIPTION, LEVEL, REALM=0, LOCAL_ITEMS=None, DOORS=None, START=False, VICTORY=False):
        RADIUS_X = LENGTH_X/2
        RADIUS_Y = LENGTH_Y/2
        self.MIN_X = X - RADIUS_X
        self.MAX_X = X + RADIUS_X
        self.MIN_Y = Y - RADIUS_Y
        self.MAX_Y = Y + RADIUS_Y
        self.LEVEL = LEVEL
        self.Z = LEVEL*2
        self.W = REALM
        self.DESCRIPTION = DESCRIPTION
        self.LOCAL_ITEMS = LOCAL_ITEMS if LOCAL_ITEMS is not None else []
        self.DOORS = DOORS if DOORS is not None else {}
        self.START = START
        self.VICTORY = VICTORY

    def ADD_ITEM(self, ITEM):
        self.LOCAL_ITEMS.append(ITEM)
        if GLOBAL_FLAGS["DEBUG"]:
            logging.debug(f"Added {ITEM.NAME} to {self.DESCRIPTION}.")

    def REMOVE_ITEM(self, ITEM):
        self.LOCAL_ITEMS.remove(ITEM)
    
    def DESCRIBE_LOCATION(self, PLAYER):
        X, Y = PLAYER.POSITION[0:2]
        LENGTH_X = (self.MAX_X - self.MIN_X)*5
        LENGTH_Y = (self.MAX_Y - self.MIN_Y)*5
        NORTH = (X-self.MIN_X)*5
        SOUTH = (self.MAX_X-X)*5
        EAST = (self.MAX_Y-Y)*5
        WEST = (Y-self.MIN_Y)*5
        
        _DESCRIPTION = f"\n\tThe {self.DESCRIPTION} is {LENGTH_Y} feet by {LENGTH_X} feet. The walls are {EAST} feet EAST, {WEST} feet WEST, {NORTH} feet NORTH, and {SOUTH} feet SOUTH."

        for key, value in self.DOORS.items():
            X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(X, Y, *value)
            X_DISTANCE, Y_DISTANCE = f"{X_DISTANCE*5} feet", f"{Y_DISTANCE*5} feet"

            _DESCRIPTION += f"\n\t{key} DOOR: {Y_DISTANCE} {Y_DIRECTION}, {X_DISTANCE} {X_DIRECTION}."
        
        for ITEM in self.LOCAL_ITEMS:
            X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(X, Y, *ITEM.POSITION[0:2])
            X_DISTANCE, Y_DISTANCE = f"{X_DISTANCE*5} feet", f"{Y_DISTANCE*5} feet"

            _DESCRIPTION += f"\n\t{ITEM.NAME}: {X_DISTANCE} {X_DIRECTION}, {Y_DISTANCE} {Y_DIRECTION}."
            if ITEM.OPEN:
                _DESCRIPTION += " OPEN."

        return _DESCRIPTION
    