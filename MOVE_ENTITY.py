def MOVE_ENTITY(POSITION, DIRECTION, DISTANCE=1):
    X, Z = POSITION

    if DIRECTION == "NORTH":
        X += DISTANCE
    elif DIRECTION == "SOUTH":
        X -= DISTANCE
    elif DIRECTION == "EAST":
        Z += DISTANCE
    elif DIRECTION == "WEST":
        Z -= DISTANCE

    return X, Z
