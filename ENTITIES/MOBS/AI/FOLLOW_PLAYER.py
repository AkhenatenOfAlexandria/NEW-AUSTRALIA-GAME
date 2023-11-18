from WORLD.GLOBAL import PLAYERS, MOBS
from LOGIC.MATH import DISTANCE
import logging


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def ATTACK_PLAYER(MOB):
    PLAYER = PLAYERS[0]
    if not PLAYER:
        return
    PLAYER_X, PLAYER_Y = PLAYER.POSITION[0:2]
    MOB_X, MOB_Y = MOB.POSITION[0:2]

    if DISTANCE(PLAYER_X, PLAYER_Y, MOB_X, MOB_Y) > 1:
        FOLLOW_PLAYER(MOB)
    else:
        MOB.COMBAT_CHECK(PLAYER)


def FOLLOW_PLAYER(MOB):
    PLAYER = PLAYERS[0]
    PLAYER_X, PLAYER_Y = PLAYER.POSITION[0:2]
    MOB_X, MOB_Y = MOB.POSITION[0:2]
    DIRECTION = {"LEFT":False, "RIGHT":False, "UP":False, "DOWN":False}
    
    if PLAYER_X-MOB_X > 0:
        DIRECTION["RIGHT"] = True
    elif MOB_X-PLAYER_X > 0:
        DIRECTION["LEFT"] = True
    elif PLAYER_Y-MOB_Y > 0:
        DIRECTION["UP"] = True
    elif MOB_Y-PLAYER_Y > 0:
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

