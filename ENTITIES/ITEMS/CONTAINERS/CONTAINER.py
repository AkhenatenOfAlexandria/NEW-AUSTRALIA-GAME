from ENTITIES.ITEMS.ITEM import ITEM
from WORLD.GLOBAL import CONTAINERS, ADD_ENTITY


class CONTAINER(ITEM):

    def __init__(self, TYPE, SIZE, POSITION, CONTENTS=None, *args, **kwargs):
        super().__init__(TYPE, POSITION, *args, **kwargs)
        self.SIZE = SIZE
        self.CONTENTS = CONTENTS if CONTENTS is not None else []
        self.OPEN = False
        self.GOLD = 0
        ADD_ENTITY(self, CONTAINERS)


    def ADD_ITEM(self, _ITEM):
        self.CONTENTS.append(_ITEM)

    def REMOVE_ITEM(self, _ITEM):
        self.CONTENTS.remove(_ITEM)


    def VIEW_CONTENTS(self):
        print(f"{self.NAME}:")
        if self.GOLD:
            print(f"GOLD: {self.GOLD}")
        for item in self.CONTENTS:
            print(item.NAME)
