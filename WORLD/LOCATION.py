from LOGIC.MATH import RELATIVE_LOCATION

class LOCATION:

    def __init__(self, MIN_X, MAX_X, MAX_Y, MIN_Y, DESCRIPTION, ENTITIES=[], DOORS={}):
        self.MIN_X = MIN_X
        self.MAX_X = MAX_X
        self.MIN_Y = MIN_Y
        self.MAX_Y = MAX_Y
        self.DESCRIPTION = DESCRIPTION
        self.ENTITIES = ENTITIES
        self.DOORS = DOORS

    def ADD_ENTITY(self, ENTITY):
        self.ENTITIES.append(ENTITY)

    def REMOVE_ENTITY(self, ENTITY):
        self.ENTITIES.remove(ENTITY)
    
    def DESCRIBE_LOCATION(self, PLAYER):
        X, Y = PLAYER.POSITION[0:2]
        LENGTH_X = (self.MAX_X - self.MIN_X)*5
        LENGTH_Y = (self.MAX_Y - self.MIN_Y)*5
        NORTH = (X-self.MIN_X)*5
        SOUTH = (self.MAX_X-X)*5
        EAST = (self.MAX_Y-Y)*5
        WEST = (Y-self.MIN_Y)*5
        
        DESCRIPTION = f"\n\tThe {self.DESCRIPTION} is {LENGTH_X} feet by {LENGTH_Y} feet. The walls are {NORTH} feet NORTH, {SOUTH} feet SOUTH, {EAST} feet EAST, and {WEST} feet WEST."

        for key, value in self.DOORS.items():
            X_DISTANCE, Y_DISTANCE, X_DIRECTION, Y_DIRECTION = RELATIVE_LOCATION(X, Y, *value)
            X_DISTANCE, Y_DISTANCE = f"{X_DISTANCE*5} feet", f"{Y_DISTANCE*5} feet"

            DESCRIPTION += f" The {key} DOOR is {X_DISTANCE} {X_DIRECTION}, {Y_DISTANCE} {Y_DIRECTION}."

        return DESCRIPTION
    