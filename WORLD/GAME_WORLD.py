from WORLD.LOCATIONS.SMALL_ROOM import SMALL_ROOM
from WORLD.LOCATIONS.CORRIDOR import CORRIDOR
from WORLD.GLOBAL import GLOBAL_FLAGS
from LOGIC.MATH import OVERLAP
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

LEVEL = GLOBAL_FLAGS["LEVEL"]

infinity = float('inf')

CENTRAL_ROOM = SMALL_ROOM(0, 0, 1, DOORS={
        "NORTH" : (-3, 0),
        "SOUTH": (3, 0),
        "WEST": (0, -3)
        },
        START=True
    )
SOUTH_CORRIDOR = CORRIDOR(17, 0, "X", 1, DOORS={"NORTH":(3, 0), "SOUTH": (31, 0)})
SOUTH_ROOM = SMALL_ROOM(34, 0, LEVEL, DOORS={"NORTH": (31, 0)})
NORTH_CORRIDOR = CORRIDOR(-17, 0, "X", 1, DOORS={"SOUTH":(-3, 0), "NORTH": (-31, 0)})
NORTH_ROOM = SMALL_ROOM(-34, 0, LEVEL, DOORS={"SOUTH": (-31, 0)})
WEST_CORRIDOR = CORRIDOR(0, -17, "Y", 1, DOORS={"EAST":(0, -3), "WEST": (0, -31)})
WEST_ROOM = SMALL_ROOM(0, -34, 1, VICTORY=True)

GAME_WORLD = [None, [
        CENTRAL_ROOM,
        SOUTH_CORRIDOR,
        SOUTH_ROOM,
        NORTH_CORRIDOR,
        NORTH_ROOM,
        WEST_CORRIDOR,
        WEST_ROOM
    ]
]


def CREATE_LEVEL():
    global GLOBAL_FLAGS
    LEVEL = GLOBAL_FLAGS["LEVEL"]
    DEBUG = GLOBAL_FLAGS["DEBUG"]
    _START = GAME_WORLD[LEVEL-1][-1]
    START_X = (_START.MIN_X + _START.MAX_X)/2
    START_Y = (_START.MIN_Y + _START.MAX_Y)/2
    _CENTRAL_ROOM = SMALL_ROOM(START_X, START_Y, LEVEL, START=True)
    NEW_LEVEL = [_CENTRAL_ROOM]
    RANGE = LEVEL+2
    for i in range(1, RANGE+1):
        print(f"GENERATING ROOMS: {i*2}/{RANGE*2}")
        PREVIOUS = random.choice(NEW_LEVEL)
        while type(PREVIOUS) != SMALL_ROOM:
            PREVIOUS = random.choice(NEW_LEVEL)
        PREVIOUS_X = (PREVIOUS.MAX_X+PREVIOUS.MIN_X)/2
        PREVIOUS_Y = (PREVIOUS.MAX_Y+PREVIOUS.MIN_Y)/2
        COUNT = 0
        while True:
            DIRECTIONS = ["NORTH", "SOUTH", "EAST", "WEST"]
            DIRECTION = random.choice(DIRECTIONS)
            if DEBUG:
                logging.debug(DIRECTION)
            if DIRECTION == "NORTH":
                X = PREVIOUS.MIN_X-14
                X2 = X-17
                Y = PREVIOUS_Y
                Y2 = Y
                LONG = "X"
                ENTRANCE = (PREVIOUS.MIN_X, Y)
                ENTRANCE_DIRECTION = "SOUTH"
                EXIT = (X-14, Y)
            elif DIRECTION == "SOUTH":
                X = PREVIOUS.MAX_X+14
                X2 = X+17
                Y = PREVIOUS_Y
                Y2 = Y
                LONG = "X"
                ENTRANCE = (PREVIOUS.MAX_X, Y)
                ENTRANCE_DIRECTION = "NORTH"
                EXIT = (X+14, Y)
            elif DIRECTION == "EAST":
                X = PREVIOUS_X
                X2 = X
                Y = PREVIOUS.MAX_Y + 14
                Y2 = Y-17
                LONG = "Y"
                ENTRANCE = (X, PREVIOUS.MAX_Y)
                ENTRANCE_DIRECTION = "WEST"
                EXIT = (X, Y+14)
            else:
                X = PREVIOUS_X
                X2 = X
                Y = PREVIOUS.MIN_Y - 14
                Y2 = Y-17
                LONG = "Y"
                ENTRANCE = (X, PREVIOUS.MIN_Y)
                ENTRANCE_DIRECTION = "EAST"
                EXIT = (X, Y-14)

            if Y > 0:
                if DEBUG:
                    logging.debug(f"{i}/{RANGE} failed. {X, Y}")
            else:
                _CORRIDOR = CORRIDOR(X, Y, LONG, LEVEL, DOORS = {
                    ENTRANCE_DIRECTION : ENTRANCE,
                    DIRECTION : EXIT
                    }
                )

                if i == RANGE:
                    _VICTORY = True
                else:
                    _VICTORY = False

                _SMALL_ROOM = SMALL_ROOM(X2, Y2, LEVEL, VICTORY=_VICTORY, DOORS = {
                    ENTRANCE_DIRECTION : EXIT
                    }
                )
                
                A = _CORRIDOR.MIN_X, _CORRIDOR.MIN_Y, _CORRIDOR.MAX_X, _CORRIDOR.MAX_Y
                B = _SMALL_ROOM.MIN_X, _SMALL_ROOM.MIN_Y, _SMALL_ROOM.MAX_X, _SMALL_ROOM.MAX_Y
                _OVERLAP = False
                for ROOM in NEW_LEVEL:
                    C = ROOM.MIN_X, ROOM.MIN_Y, ROOM.MAX_X, ROOM.MAX_Y
                    if OVERLAP(A, C):
                        OVERLAP_REASON = (f"CORRIDOR at {X, Y} overlaps {ROOM.DESCRIPTION} at {(ROOM.MIN_X+ROOM.MAX_X)/2, (ROOM.MIN_Y+ROOM.MAX_Y)/2}.")
                        _OVERLAP = True
                        break
                    if OVERLAP(B, C):
                        OVERLAP_REASON = (f"SMALL ROOM at {X, Y} overlaps {ROOM.DESCRIPTION} at {(ROOM.MIN_X+ROOM.MAX_X)/2, (ROOM.MIN_Y+ROOM.MAX_Y)/2}.")
                        _OVERLAP = True
                        break
                if not _OVERLAP:
                    PREVIOUS.DOORS[DIRECTION] = ENTRANCE
                    NEW_LEVEL.append(_CORRIDOR)
                    NEW_LEVEL.append(_SMALL_ROOM)
                    if DEBUG:
                        logging.debug(f"{i*2}/{RANGE*2} generated: {X, Y}, {X2, Y2}.")
                    break
                else:
                    if DEBUG:
                        logging.debug(f"{i}/{RANGE} failed: {OVERLAP_REASON}")
            COUNT += 1
            if DEBUG and COUNT > 100:
                for ROOM in NEW_LEVEL:
                    logging.debug(ROOM.DESCRIPTION, (ROOM.MIN_X+ROOM.MAX_X)/2, (ROOM.MIN_Y+ROOM.MAX_Y)/2)
                input()
                COUNT = 0
            if not DEBUG and COUNT > 1024:
                if _SMALL_ROOM.VICTORY:
                    NEW_LEVEL[-1].VICTORY = True
                break
                    

    GAME_WORLD.append(NEW_LEVEL)
    if DEBUG:
        for ROOM in NEW_LEVEL:
            logging.debug(f"{ROOM.DESCRIPTION}: {(ROOM.MIN_X+ROOM.MAX_X)/2}, {(ROOM.MIN_Y+ROOM.MAX_Y)/2}")
        input()