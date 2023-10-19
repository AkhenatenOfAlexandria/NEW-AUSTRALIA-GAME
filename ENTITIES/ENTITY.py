 
class ENTITY:

    def __init__(self, TYPE, POSITION=None, *args, **kwargs):
        self.POSITION = POSITION
        self.ARMOR_CLASS = 1
        self.INVENTORY = {"ITEMS":[]}
        self.TYPE = TYPE
        self.ATTRIBUTES = set(args)