 
class ENTITY:

    def __init__(self, POSITION, *args, **kwargs):
        self.POSITION = POSITION
        self.ARMOR_CLASS = 1
        self.INVENTORY = {"ITEMS":[]}
        
        self.ATTRIBUTES = set(args)