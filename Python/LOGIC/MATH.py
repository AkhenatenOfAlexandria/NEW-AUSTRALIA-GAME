import math
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def VECTOR_DIRECTION_RADIANS(X, Y):   
    # Calculate the angle in radians using atan2
    angle_radians = math.atan2(X, Y)

    while angle_radians < 0:
        angle_radians += 2 * math.pi
    while angle_radians >= 2 * math.pi:
        angle_radians -= 2 * math.pi

    return angle_radians

def VECTOR_DIRECTION(X, Y):
    radians = VECTOR_DIRECTION_RADIANS(X, Y)
    if radians <= math.pi/4 or radians > math.pi*7/4:
        return "EAST"
    elif math.pi/4 < radians <= math.pi*3/4:
        return "SOUTH" #east
    elif math.pi*3/4 < radians <= math.pi*5/4:
        return "WEST" #south
    elif math.pi*5/4 < radians <= math.pi * 7/4:
        return "NORTH"
    

def ROLL(COUNT, DIE, *args, **kwargs):
    RESULT = 0
    for i in range(COUNT):
        RESULT += random.randint(1, DIE)
    return RESULT


def POSITION_CORNERS(X, Y):
    UPPER_LEFT_CORNER = (X*5-2.5, Y*5+2.5)
    UPPER_RIGHT_CORNER = (X*5+2.5, Y*5+2.5)
    LOWER_RIGHT_CORNER = (X*5+2.5, Y*5-2.5)
    LOWER_LEFT_CORNER = (X*5-2.5, Y*5-2.5)
    CORNERS = (UPPER_LEFT_CORNER, UPPER_RIGHT_CORNER, LOWER_RIGHT_CORNER, LOWER_LEFT_CORNER)
    return CORNERS


def OVERLAP(A, B):
    AX1, AY1, AX2, AY2 = A
    BX1, BY1, BX2, BY2 = B

    if AX1 >= BX2:
        # logging.debug(f"{AX1} >= {BX2}.")
        return False
    if AY1 >= BY2:
        # logging.debug(f"{AY1} >= {BY2}.")
        return False
    if AX2 <= BX1:
        # logging.debug(f"{AX2} <= {BX1}.")
        return False
    if AY2 <= BY1:
        # logging.debug(f"{AY2} <= {BY1}.")
        return False
    else:
        # logging.debug("Overlap found.")
        return True


def SLOPE(X0, X1, Y0, Y1):
    return (Y1-Y0)/(X1-X0)

def RELATIVE_LOCATION(X0, Y0, X1, Y1):
    X_DISTANCE = abs(X1-X0)
    Y_DISTANCE = abs(Y1-Y0)
    if X1-X0 >= 0:
        X_DIRECTION = "SOUTH"
    else:
        X_DIRECTION = "NORTH"
    if Y1-Y0 >= 0:
        Y_DIRECTION = "EAST"
    else:
        Y_DIRECTION = "WEST"
    return X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION


def DISTANCE(X1, Y1, X2, Y2):
    DX = X2 - X1
    DY = Y2 - Y1
    return math.sqrt(DX**2 + DY**2)


def MELEE_RANGE(MOB_X, MOB_Y, ENEMY_X, ENEMY_Y, REACH=1):
    X_DISTANCE = abs(ENEMY_X - MOB_X)
    Y_DISTANCE = abs(ENEMY_Y - MOB_Y)
    _DISTANCE = DISTANCE(MOB_X, MOB_Y, ENEMY_X, ENEMY_Y)

    if X_DISTANCE <= REACH and Y_DISTANCE <= REACH:
        return True
    elif _DISTANCE <= REACH:
        return True
    return False
