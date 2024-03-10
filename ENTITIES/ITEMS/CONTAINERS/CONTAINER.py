from ENTITIES.ITEMS.ITEM import ITEM
from WORLD.GLOBAL import CONTAINERS, ADD_ENTITY, UPDATE_DISPLAY, DISPLAY

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


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
        logging.info(f"Removed {_ITEM.NAME} from {self.NAME}.")


    def VIEW_CONTENTS(self):
        DISPLAY = f"\n\n{self.NAME}:"
        if self.GOLD:
            DISPLAY+=f"\n     GOLD: {self.GOLD}"
        for item in self.CONTENTS:
            DISPLAY += f"\n     {self.CONTENTS.index(item)}. {item.DESCRIPTION}"
        UPDATE_DISPLAY("INFO", DISPLAY)


    def OPEN_CONTAINER(self):
        self.OPEN = True
        self.VIEW_CONTENTS()
    

    def CLOSE_CONTAINER(self):
        self.OPEN = False
        UPDATE_DISPLAY("INFO", f"\n\nClosed {self.NAME}.")
