import math
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def PASSED(X1, Y1, X2, Y2, X, Y):
    if X and X2 >= X1:
            return True
    elif X1 >= X2:
        return True
    if Y and Y2 >= Y1:
        return True
    elif Y1 >= Y2:
        return True
    return False


def CHOOSE_LOOT(TABLE):
    logging.debug(f"INITIATING CHOOSE_LOOT(). {TABLE}")
    RAND = random.random()
    logging.debug(f"RAND: {RAND}")
    CUMULATIVE = 0
    COUNT = 0
    for ITEM, WEIGHT in TABLE.items():
        COUNT +=1
        logging.debug(f"{COUNT}: {ITEM} of WEIGHT {WEIGHT}.")
        CUMULATIVE += WEIGHT
        if CUMULATIVE >= RAND:
            if ITEM:
                logging.debug(f"LOOT CHOSEN: {ITEM}.")
                return ITEM
            else:
                logging.error(f"No loot generated. {TABLE}")


def NUMBERS_LOOT_TABLE(NUMBER):
    TOTAL = 0
    WEIGHTS = []
    for i in range(1, NUMBER+1):
        TOTAL += 1/i
    for i in range (1, NUMBER+1):
        WEIGHT = (1/i)/TOTAL
        WEIGHTS.append(WEIGHT)
    return WEIGHTS


def CHOOSE_NUMBER(WEIGHTS):
    RAND = random.random()
    CUMULATIVE = 0
    
    for i in range(1, len(WEIGHTS)+1):
        CUMULATIVE += WEIGHTS[i-1]
        if CUMULATIVE >= RAND:
            return i


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
