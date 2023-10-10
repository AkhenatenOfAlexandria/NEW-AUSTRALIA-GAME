from ENTITIES.ENTITY import ENTITY

class CHEST(ENTITY):
    CHESTS = []

    def __init__(self
                 # POSITION,
                 # CONTENTS
                 ):
        # self.POSITION = POSITION
        # self.CONTENTS = CONTENTS
        CHEST.CHESTS.append(self)

    def ADD_ITEM(self, ITEM):
        self.CONTENTS.append(ITEM)

    def REMOVE_ITEM(self, ITEM):
        self.CONTENTS.remove(ITEM)

    def __str__(self):
        return f'CHEST: {self.POSITION}, CONTENTS: {", ".join(self.CONTENTS)}'