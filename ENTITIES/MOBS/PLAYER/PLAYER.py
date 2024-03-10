from ENTITIES.MOBS.MOB import MOB
import WORLD.GAME_WORLD as _WORLD
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL, DISTANCE
from WORLD.GLOBAL import MOBS, PLAYERS, ADD_ENTITY, DISPLAY, UPDATE_FLAG, CONTAINERS, UPDATE_DISPLAY, REMOVE_ENTITY
from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

import tcod.console
import tcod.event


class PLAYER(MOB):

    def __init__(
            self,
            POSITION=[0,0,0,0],
            STRENGTH=16,
            DEXTERITY=14,
            CONSTITUTION=15,
            INTELLIGENCE=13,
            WISDOM=11,
            CHARISMA=9,
            HEALTH=10,
            *args, **kwargs
            ):
        
        super().__init__(
            POSITION,
            STRENGTH,
            DEXTERITY,
            CONSTITUTION,
            INTELLIGENCE,
            WISDOM,
            CHARISMA,
            HEALTH,
            "PLAYER",
            2,
            "DEFENSE",
            *args, **kwargs
            )
        
        ADD_ENTITY(self, PLAYERS)

        self.NAME = f"PLAYER {self.MOB_ID}"
        self.CHARACTER = str(self.MOB_ID)

        self.INVENTORY["GOLD"] = 10.0

        self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

        self.EXPERIENCE = 0
        self.EXPERIENCE_LEVEL = 1

        self.SPEED = 6

        if not self.ATTRIBUTES:
            self.ATTRIBUTES = set("DEFENSE")
        

    def XP_LEVEL(self):
        _POINTS = self.EXPERIENCE
        _LEVEL = self.EXPERIENCE_LEVEL
        _LEVELS = {
            1: 0,
            2: 300,
            3: 900,
            4: 2700,
            5: 6500,
            6: 14000,
            7: 23000,
            8: 34000,
            9: 48000,
            10: 64000,
            11: 85000,
            12: 100000,
            13: 120000,
            14: 140000,
            15: 165000,
            16: 195000,
            17: 225000,
            18: 265000,
            19: 305000,
            20: 355000}
        
        for key, value in _LEVELS.items():
            if _POINTS >= value:
                _LEVEL = key
                if _LEVEL > self.EXPERIENCE_LEVEL:
                    self.EXPERIENCE_LEVEL = _LEVEL
                    HP = max((ROLL(1, 10) + self.CONSTITUTION_MODIFIER), 1)
                    self.MAX_HEALTH += HP
            else:
                break
    
    
    def ROOM_CHECK(self):
        for mob in MOBS:
            if mob and LOCATION_ID(*mob.POSITION[0:2]) == LOCATION_ID(*self.POSITION[0:2]) and mob != self:
                return True
        return False
    

    def UPDATE(self, MOVE, NUM):
        _LOCATION = LOCATION_ID(*self.POSITION[0:2])
        if MOVE in ["LEFT", "RIGHT", "UP", "DOWN"]:
            self._MOVE(MOVE, _LOCATION)
        elif MOVE == "SPACE":
            self.SPACE(_LOCATION)
        elif MOVE == "LOOT":
            self.LOOT()
        elif MOVE == "DROP":
            self.DROP_ITEM(NUM)
        elif MOVE == "EQUIP":
            self.EQUIP_ITEM(NUM)
    

    def _MOVE(self, MOVE, _LOCATION):
        POSITION = self.MOVE(MOVE)
        STAY = False
        for MOB in MOBS:
            if MOB and POSITION == MOB.POSITION[0:2]:
                STAY = True
                self.COMBAT_CHECK(MOB)
                break
        if not STAY:
            OLD_POSITION = self.POSITION[0:2]
            self.POSITION[0:2] = POSITION
            DIFFERENCE = (POSITION[0]-OLD_POSITION[0], POSITION[1]-OLD_POSITION[1])
            _LOCATION.FOUND = True
            if self.ATTACHED and (
                (abs(POSITION[0]-self.ATTACHED.POSITION[0]) > 1
                    ) or (
                    abs(POSITION[1]-self.ATTACHED.POSITION[1]) > 1
                    )):
                self.ATTACHED.POSITION[0] += DIFFERENCE[0]
                self.ATTACHED.POSITION[1] += DIFFERENCE[1]

    
    def SPACE(self, _LOCATION):
        if self.PRONE:
            self.PRONE = False
            UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+f"\n{self.NAME} is no longer PRONE.")
        if _LOCATION.VICTORY:
                UPDATE_FLAG("NEW LEVEL", True)
        elif len(_LOCATION.LOCAL_ITEMS):
            for ITEM in _LOCATION.LOCAL_ITEMS:
                if ITEM in CONTAINERS and DISTANCE(*self.POSITION[0:2], *ITEM.POSITION[0:2]) < 2:
                    if ITEM.OPEN:
                        ITEM.CLOSE_CONTAINER()
                    else:
                        ITEM.OPEN_CONTAINER()

    def OPEN_INVENTORY(self):
        _DISPLAY = "\n"
        _DISPLAY += f"\nEXPERIENCE LEVEL: {self.EXPERIENCE_LEVEL}"
        _DISPLAY += f"\nEXPERIENCE POINTS: {self.EXPERIENCE}"
        _DISPLAY += "\nINVENTORY:"
        if self.INVENTORY["WEAPON"]:
            WEAPON = self.INVENTORY["WEAPON"].DESCRIPTION
            _DISPLAY += f"\n     WEAPON: {WEAPON}"
        else:
            _DISPLAY += f"\n     WEAPON: None."
        if self.INVENTORY["ARMOR"]:
            ARMOR = self.INVENTORY["ARMOR"].DESCRIPTION
        else:
            ARMOR = None
        _DISPLAY += f"\n     ARMOR: {ARMOR}"
        if self.INVENTORY["SHIELD"]:
            _DISPLAY += "\n     SHIELD"
        _DISPLAY += f"\n     GOLD: {self.INVENTORY['GOLD']}"
        _DISPLAY += f"\n     ITEMS:"
        
        for ITEM in self.INVENTORY["ITEMS"]:
            _DISPLAY += f"\n          {self.INVENTORY['ITEMS'].index(ITEM)}. {ITEM.DESCRIPTION}"
        
        UPDATE_DISPLAY("INFO", _DISPLAY)
    

    def SELECT_ITEM(self):
        self.OPEN_INVENTORY()
        _DISPLAY = DISPLAY["INFO"]
        _DISPLAY += "\n\nSELECT ITEM"
        UPDATE_DISPLAY("INFO", _DISPLAY)

    
    def DROP_ITEM(self, NUM):
        _ITEMS = self.INVENTORY["ITEMS"]

        try:
            _ITEM = _ITEMS.pop(NUM)
            _ITEM.POSITION = self.POSITION
            _DISPLAY = f"\nDROPPED {_ITEM.NAME}"
            
            UPDATE_DISPLAY("INFO", _DISPLAY)

        except IndexError as e:
            logging.debug(f"IndexError: {e}")
            logging.debug(f"NUM: {NUM}\nITEMS:{_ITEMS}")
        

    
    def EQUIP_ITEM(self, NUM):
        _ITEMS = self.INVENTORY["ITEMS"]
        
        try:
            _ITEM = _ITEMS[NUM]
            if isinstance(_ITEM, MELEE_WEAPON):
                _WEAPON = self.INVENTORY["WEAPON"]
                if _WEAPON:
                    _ITEMS.append(_WEAPON)
                self.INVENTORY["WEAPON"] = _ITEM
                _ITEMS.remove(_ITEM)
                _DISPLAY = f"\nEQUIPPED {_ITEM.NAME}"
            elif _ITEM.TYPE == "SHIELD":
                _SHIELD = self.INVENTORY["SHIELD"]
                if _SHIELD:
                    _ITEMS.append(_SHIELD)
                self.INVENTORY["SHIELD"] = _ITEM
                _ITEMS.remove(_ITEM)
                _DISPLAY = f"\nEQUIPPED {_ITEM.NAME}"
            
            UPDATE_DISPLAY("INFO", _DISPLAY)

        except IndexError as e:
            logging.debug(f"IndexError: {e}")
            logging.debug(f"NUM: {NUM}\nITEMS:{_ITEMS}")
        
    
    def LOOT(self):
        _LOCATION = LOCATION_ID(*self.POSITION[0:2])
        if len(_LOCATION.LOCAL_ITEMS):
            for ITEM in _LOCATION.LOCAL_ITEMS:
                if ITEM in CONTAINERS and DISTANCE(*self.POSITION[0:2], *ITEM.POSITION[0:2]) < 2 and ITEM.OPEN:
                    if ITEM.GOLD:
                        self.INVENTORY["GOLD"] += ITEM.GOLD
                        ITEM.GOLD = 0
                    while len(ITEM.CONTENTS) and len(self.INVENTORY["ITEMS"]) < 10:
                        _ITEM = ITEM.CONTENTS[0]
                        self.INVENTORY["ITEMS"].append(_ITEM)
                        ITEM.REMOVE_ITEM(_ITEM)
                    ITEM.VIEW_CONTENTS()
    

    def DIE(self):
        _GOLD = self.INVENTORY["GOLD"]
        _WEAPON = self.INVENTORY["WEAPON"]
        _ARMOR = self.INVENTORY["ARMOR"]
        if _WEAPON:
            _WEAPON.POSITION = self.POSITION
            _GOLD += _WEAPON.PRICE
        if _ARMOR:
            _ARMOR.POSITION = self.POSITION
            _GOLD += _ARMOR.PRICE
        for ITEM in self.INVENTORY["ITEMS"]:
            ITEM.POSITION = self.POSITION
            _GOLD += ITEM.PRICE
        UPDATE_FLAG("SCORE", self.EXPERIENCE)
        UPDATE_FLAG("GOLD", _GOLD)
        MESSAGE = f"{self.NAME} died."
        logging.info(MESSAGE)
        REMOVE_ENTITY(self)

        return True
    