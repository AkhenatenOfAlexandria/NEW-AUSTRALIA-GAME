import math
import random

def VECTOR_DIRECTION_RADIANS(X, Y):   
    # Calculate the angle in radians using atan2
    angle_radians = math.atan2(Y, X)

    while angle_radians < 0:
        angle_radians += 2 * math.pi
    while angle_radians >= 2 * math.pi:
        angle_radians -= 2 * math.pi

    return angle_radians

def VECTOR_DIRECTION(X, Y):
    radians = VECTOR_DIRECTION_RADIANS(X, Y)
    if radians <= math.pi/4 or radians > math.pi*7/4:
        return "NORTH"
    elif math.pi/4 < radians <= math.pi*3/4:
        return "EAST" #east
    elif math.pi*3/4 < radians <= math.pi*5/4:
        return "SOUTH" #south
    elif math.pi*5/4 < radians <= math.pi * 7/4:
        return "WEST"
    

def ROLL(COUNT, DIE, *args):
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


def SLOPE(X0, X1, Y0, Y1):
    return (Y1-Y0)/(X1-X0)
