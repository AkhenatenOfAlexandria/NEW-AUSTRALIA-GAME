import logging

import ENTITIES.MOBS.AI.FOLLOW_PLAYER as FOLLOW_PLAYER
from WORLD.GLOBAL import GLOBAL_FLAGS, INITIATIVE_MOBS, PLAYERS
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import MELEE_RANGE

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def ATTACK_PLAYER(MOB):
    global GLOBAL_FLAGS
    DEBUG = GLOBAL_FLAGS["DEBUG"]
    GAME_RUNNING = True
    for mob in reversed(INITIATIVE_MOBS):
        if mob in PLAYERS:
            PLAYER = mob
        else:
            PLAYER = PLAYERS[0]
    if DEBUG:
        logging.debug(f"{MOB.NAME} attacking {PLAYER.NAME}.")
    DIRECTION = FOLLOW_PLAYER.DIRECTION(PLAYER, MOB)
    MOB_LOCATION = LOCATION_ID(*MOB.POSITION[0:2])
    PLAYER_LOCATION = LOCATION_ID(*PLAYER.POSITION[0:2])
    if MOB_LOCATION != PLAYER_LOCATION:
        pass

    else:
        ACTION = True
        MOVEMENT = 1
        while (ACTION or MOVEMENT) and GAME_RUNNING:
            IN_RANGE = MELEE_RANGE(*MOB.POSITION[0:2], *PLAYER.POSITION[0:2])
            if IN_RANGE and ACTION:
                try:
                    GAME_RUNNING = MOB.COMBAT_CHECK(PLAYER)
                    ACTION = False
                    if DEBUG:
                        logging.debug(f"{MOB.NAME} used ACTION.")
                except TypeError as e:
                    logging.error(f"TypeError: {e}.")
                    GAME_RUNNING = False
            
            elif (ACTION or MOVEMENT) and not IN_RANGE:
                if DEBUG:
                    logging.debug(f"{MOB.NAME} attempting to move {DIRECTION}.")
                FOLLOW_PLAYER.MOVE(PLAYER, MOB, DIRECTION)
                if MOVEMENT:
                    MOVEMENT = 0
                    logging.debug(f"{MOB.NAME} used MOVEMENT.")
                else:
                    ACTION = False
                    if DEBUG:
                        logging.debug(f"{MOB.NAME} used DASH ACTION.")
            else:
                if DEBUG:
                    logging.debug(f"{MOB.NAME} cedes MOVEMENT.")
                break

    return GAME_RUNNING, False