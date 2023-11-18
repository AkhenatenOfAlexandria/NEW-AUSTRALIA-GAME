from WORLD.GLOBAL import PLAYERS
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID


class ENTITY:

    def __init__(self, TYPE, POSITION=None, *args, **kwargs):
        self.POSITION = POSITION
        self.ARMOR_CLASS = 1
        self.INVENTORY = {"ITEMS":[]}
        self.TYPE = TYPE
        self.ATTRIBUTES = set(args)


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
        if DIRECTION == "LEFT":
            POSITION = [X-1, Y]
        elif DIRECTION == "RIGHT":
            POSITION = [X+1, Y]
        elif DIRECTION == "UP":
            POSITION = [X, Y+1]
        elif DIRECTION == "DOWN":
            POSITION = [X, Y-1]
        if LOCATION_ID(*POSITION):
            return POSITION
        else:
            return X, Y
