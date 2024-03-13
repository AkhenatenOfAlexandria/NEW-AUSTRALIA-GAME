import logging

from LOGIC.MATH import RELATIVE_LOCATION
from WORLD.GLOBAL import GLOBAL_FLAGS, PLAYERS

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

class LOCATION:


    def __init__(self, X, Y, LENGTH_X, LENGTH_Y, DESCRIPTION, LEVEL, REALM=0, LOCAL_ITEMS=None, DOORS=None, START=False, VICTORY=False):
        RADIUS_X = LENGTH_X/2
        RADIUS_Y = LENGTH_Y/2
        self.MIN_X = int(X - RADIUS_X)
        self.MAX_X = int(X + RADIUS_X)
        self.MIN_Y = int(Y - RADIUS_Y)
        self.MAX_Y = int(Y + RADIUS_Y)
        self.LEVEL = LEVEL
        self.Z = LEVEL*2
        self.W = REALM
        self.DESCRIPTION = DESCRIPTION
        self.LOCAL_ITEMS = LOCAL_ITEMS if LOCAL_ITEMS is not None else []
        self.DOORS = DOORS if DOORS is not None else {}
        self.START = START
        self.VICTORY = VICTORY
        self.STRING = None
        self.FOUND = False


    def ADD_ITEM(self, ITEM):
        self.LOCAL_ITEMS.append(ITEM)
        if GLOBAL_FLAGS["DEBUG"]:
            logging.debug(f"Added {ITEM.NAME} to {self.DESCRIPTION}.")


    def REMOVE_ITEM(self, ITEM):
        self.LOCAL_ITEMS.remove(ITEM)


    def _DRAW(self):
        LENGTH = int(self.MAX_X - self.MIN_X)
        HEIGHT = int(self.MAX_Y - self.MIN_Y)
        
        if "NORTH" in self.DOORS:
            NORTH_DOOR = self.DOORS["NORTH"][1] - self.MIN_Y
        if "SOUTH" in self.DOORS:
            SOUTH_DOOR = self.DOORS["SOUTH"][1] - self.MIN_Y
        if "EAST" in self.DOORS:
            EAST_DOOR = self.DOORS["EAST"][0] - self.MIN_X
        if "WEST" in self.DOORS:
            WEST_DOOR = self.DOORS["WEST"][0] - self.MIN_X

        _STRING = ""
        
        EAST_WALL = "#"
        WEST_WALL = "#"
        ROOM = "#"
        NORTH_DOOR_ROOM = "*"
        for i in range(1, LENGTH):
            if "EAST" in self.DOORS and i == EAST_DOOR:
                EAST_WALL += "*"
            else:
                EAST_WALL += "#"
            if "WEST" in self.DOORS and i == WEST_DOOR:
                WEST_WALL += "*"
            else:
                WEST_WALL += "#"
        EAST_WALL += "#"
        WEST_WALL += "#"
        for i in range(LENGTH-1):
            if self.VICTORY:
                ROOM += "+"
                NORTH_DOOR_ROOM += "+"
            elif self.START:
                ROOM += "-"
                NORTH_DOOR_ROOM += "-"
            else:
                NORTH_DOOR_ROOM += " "
                ROOM += " "
        if "SOUTH" in self.DOORS and "NORTH" in self.DOORS and NORTH_DOOR == SOUTH_DOOR:
            NORTH_DOOR_ROOM += "*"
        else:
            NORTH_DOOR_ROOM += "#"
            SOUTH_DOOR_ROOM = ROOM + "*"
        ROOM += "#"
        _STRING += EAST_WALL
        for i in range(1, HEIGHT):
            if "NORTH" in self.DOORS and i == NORTH_DOOR:
                _STRING += f"\n{NORTH_DOOR_ROOM}"
            elif "SOUTH" in self.DOORS and i== SOUTH_DOOR:
                _STRING += f"\n{SOUTH_DOOR_ROOM}"
            else:
                _STRING += f"\n{ROOM}"
        _STRING += f"\n{WEST_WALL}"
        return _STRING
    
    
    def DRAW(self, CONSOLE):
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        X = int(CONSOLE.width//2 + self.MIN_X - PLAYER.POSITION[0])
        Y = int(CONSOLE.height//2 - self.MAX_Y + PLAYER.POSITION[1])
        
        try:
            CONSOLE.print(X, Y, string=self.STRING)
            for ITEM in self.LOCAL_ITEMS:
                ITEM.DRAW(CONSOLE)
        except AttributeError as e:
            logging.error(f"AtrributeError {e}\n{self.STRING}")
    