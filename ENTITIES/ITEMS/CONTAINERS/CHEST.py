from ENTITIES.ITEMS.CONTAINERS.CONTAINER import CONTAINER

class CHEST(CONTAINER):
    
    def __init__(self, POSITION, CONTENTS=None, *args, **kwargs):
        super().__init__("CHEST", 16, POSITION, CONTENTS, *args, **kwargs)
