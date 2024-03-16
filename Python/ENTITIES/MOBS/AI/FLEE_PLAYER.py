from WORLD.GLOBAL import PLAYERS, MOBS, UPDATE_DISPLAY, DISPLAY
from LOGIC.MATH import DISTANCE, ROLL
import logging


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def FLEE_PLAYER(MOB):
    if MOB.PRONE:
        MOB.PRONE = False
    else:
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        PLAYER_X, PLAYER_Y = PLAYER.POSITION[0:2]
        MOB_X, MOB_Y = MOB.POSITION[0:2]
        DIRECTION = {"LEFT": False, "RIGHT": False, "UP": False, "DOWN": False}
        
        if MOB_X-PLAYER_X > 0:
            DIRECTION["RIGHT"] = True
        elif PLAYER_X-MOB_X > 0:
            DIRECTION["LEFT"] = True
        elif MOB_Y-PLAYER_Y > 0:
            DIRECTION["UP"] = True
        elif PLAYER_Y-MOB_Y > 0:
            DIRECTION["DOWN"] = True
        
        for key, value in DIRECTION.items():
            if value:
                STAY = False
                POSITION = MOB.MOVE(key)
                for mob in MOBS:
                    if mob and POSITION == mob.POSITION[0:2]:
                        STAY = True
                        break
                if not STAY:
                    MOB.POSITION[0:2] = POSITION
                    if MOB.ATTACHED and (
                        (abs(POSITION[0]-MOB.ATTACHED.POSITION[0]) > 1
                         ) or (
                            abs(POSITION[1]-MOB.ATTACHED.POSITION[1]) > 1
                            )):
                        MOB.ATTACHED.POSITION[0:2] = POSITION


