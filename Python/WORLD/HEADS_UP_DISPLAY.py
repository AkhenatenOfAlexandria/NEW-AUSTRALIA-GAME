from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import RELATIVE_LOCATION
from WORLD.GLOBAL import MOBS, GLOBAL_FLAGS, DISPLAY, UPDATE_DISPLAY, PLAYERS
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def INITIALIZE_DISPLAY():
    UPDATE_DISPLAY("HUD", HEADS_UP_DISPLAY())


class HEADS_UP_DISPLAY:
    

    def DRAW(self, CONSOLE):
        global DISPLAY
        TIME = GLOBAL_FLAGS["TIME"]
        LEVEL = GLOBAL_FLAGS["LEVEL"]
        INFO = DISPLAY["INFO"]
        PLAYER = PLAYERS[0]
        if not PLAYER:
            X = int(CONSOLE.width/2)
            Y = int(CONSOLE.height/2)
            CONSOLE.clear()
            CONSOLE.print(X, Y, "GAME OVER")
            return
        POSITION = PLAYER.POSITION
        HEALTH = PLAYER.HEALTH
        MAX_HEALTH = PLAYER.MAX_HEALTH
        WATER = PLAYER.WATER
        EXHAUSTION = PLAYER.EXHAUSTION
        
        X, Y = 1, 1
        while INFO.count('\n') > 20:
            INDEX = INFO.find('\n', 2)
            if INDEX != -1:
                UPDATE_DISPLAY("INFO", f"{INFO[INDEX:]}")
                INFO = DISPLAY["INFO"]            

        _DISPLAY = f"TIME: {TIME}\nLEVEL: {LEVEL}\nLOCATION: {POSITION}\nHEALTH: {HEALTH}/{MAX_HEALTH}\nEXHAUSTION: {EXHAUSTION}/6\nWATER: {WATER}/8\n{INFO}"
        CONSOLE.print(X, Y, string=_DISPLAY)
