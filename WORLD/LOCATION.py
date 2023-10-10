class LOCATION:

    def __init__(self, MIN_X, MAX_X, MAX_Z, MIN_Z, DESCRIPTION, ENTITIES=[], DOORS={}):
        self.MIN_X = MIN_X
        self.MAX_X = MAX_X
        self.MIN_Z = MIN_Z
        self.MAX_Z = MAX_Z
        self.DESCRIPTION = DESCRIPTION
        self.ENTITIES = ENTITIES
        self.DOORS = DOORS

    def ADD_ENTITY(self, ENTITY):
        self.ENTITIES.append(ENTITY)

    def REMOVE_ENTITY(self, ENTITY):
        self.ENTITIES.remove(ENTITY)
