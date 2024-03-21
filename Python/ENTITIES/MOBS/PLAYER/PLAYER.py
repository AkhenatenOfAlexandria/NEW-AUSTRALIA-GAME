from ENTITIES.MOBS.MOB import MOB
import WORLD.GAME_WORLD as _WORLD
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL, DISTANCE
from WORLD.GLOBAL import MOBS, PLAYERS, ADD_ENTITY, DISPLAY, UPDATE_FLAG, CONTAINERS, UPDATE_DISPLAY, REMOVE_ENTITY, GLOBAL_FLAGS
from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON
from ENTITIES.ITEMS.RANGED_WEAPONS.RANGED_WEAPON import RANGED_WEAPON
from ENTITIES.ITEMS.ARMOR.ARMOR import ARMOR
from LOGIC.FUNCTIONS import SORT_MOBS, SORT_MOBS_MELEE
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID

import logging
import random
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


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

        self.INVENTORY["GOLD"] = 0.0

        self.ARMOR_CLASS = self.ARMOR_CLASS_CALCULUS()

        self.EXPERIENCE = 0
        self.EXPERIENCE_LEVEL = 1

        self.SPEED = 6

        if not self.ATTRIBUTES:
            self.ATTRIBUTES = set("DEFENSE")

        self.MAX_WATER = 16
        self.WATER = 8

        self.LONG_REST = 0
        self.HIT_DICE = 1
        self.MAX_HIT_DICE = 1

        self.PERCEPTION_CHECK = False
        

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
                    self.MAX_HIT_DICE += 1
            else:
                break
    
    
    def ROOM_CHECK(self):
        for mob in MOBS:
            if mob and LOCATION_ID(*mob.POSITION[0:2]) == LOCATION_ID(*self.POSITION[0:2]) and mob != self:
                return True
        return False
    

    def UPDATE(self, MOVE, NUM=None, VERSATILE=False, HANDS=None):
        logging.debug(f"UPDATING PLAYER: {MOVE}.")
        self.PERCEPTION_CHECK = False
        _LOCATION = LOCATION_ID(*self.POSITION[0:2])
        TIME = GLOBAL_FLAGS["TIME"]
        if TIME and TIME % 10800 == 0:
            if self.WATER:
                self.WATER -= 1
            else:
                self.HEALTH -= 1
        if TIME and TIME % 86400 == 0:
            if self.WATER < 4:
                self.EXHAUSTION += 1
            elif 8 > self.WATER >= 4:
                THROW = ROLL(1, 20)
                if self.EXHAUSTION >= 3:
                    THROW = min(THROW, ROLL(1,20))
                if THROW + self.CONSTITUTION_MODIFIER < 15:
                    self.EXHAUSTION += 1
        if self.HEALTH <= 0 or self.EXHAUSTION >= 6:
            self.DIE()
        if MOVE in ["LEFT", "RIGHT", "UP", "DOWN"]:
            self._MOVE(MOVE, _LOCATION)
        elif MOVE == "SPACE":
            self.SPACE(_LOCATION)
        elif MOVE == "LOOT":
            self.LOOT()
        elif MOVE == "DROP":
            self.DROP_ITEM(NUM)
        elif MOVE in ("EQUIP", "VERSATILE"):
            if NUM == "F":
                logging.debug("ATTEMPTING TO EQUIP F: MOVING.")
            if self.EQUIP_ITEM(NUM, VERSATILE, HANDS):
                return "VERSATILE"
        elif MOVE == "RANGED_ATTACK":
            try:
                self.RANGED_ATTACK(SORT_MOBS(self)[NUM])
            except IndexError:
                logging.error("Invalid target.")
        elif MOVE == "MELEE_ATTACK":
            try:
                if self.INVENTORY["WEAPON"] and "REACH" in self.INVENTORY["WEAPON"].ATTRIBUTES:
                    REACH = True
                else:
                    REACH = False
                self.COMBAT_CHECK(SORT_MOBS_MELEE(self, REACH)[NUM])
            except IndexError:
                logging.error("Invalid target.")
        elif MOVE == "DRINK":
            self.DRINK()
    

    def _MOVE(self, MOVE, _LOCATION):
        POSITION = self.MOVE(MOVE)
        STAY = False
        for MOB in MOBS:
            if MOB and POSITION == MOB.POSITION[0:2]:
                STAY = True
                if MOB.SEEN:
                    self.COMBAT_CHECK(MOB)
                else:
                    MOB.SEEN = True
                break
        if not STAY:
            MULTIPLIER = 1
            if self.PRONE:
                MULTIPLIER *= 0.5
            if self.EXHAUSTION >= 2:
                MULTIPLIER *= 0.5
            if random.random() > MULTIPLIER or self.EXHAUSTION >= 5:
                return
            OLD_POSITION = self.POSITION[0:2]
            self.POSITION[0:2] = POSITION
            STEALTH = ROLL(1,20)
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
        logging.debug("SPACE activated.")
        if self.PRONE:
            self.PRONE = False
            UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+f"\n{self.NAME} is no longer PRONE.")
            return
        if _LOCATION.VICTORY:
            UPDATE_FLAG("NEW LEVEL", True)
            return
        elif len(_LOCATION.LOCAL_ITEMS):
            for ITEM in _LOCATION.LOCAL_ITEMS:
                if ITEM in CONTAINERS and DISTANCE(*self.POSITION[0:2], *ITEM.POSITION[0:2]) < 2:
                    if ITEM.OPEN:
                        ITEM.CLOSE_CONTAINER()
                    else:
                        ITEM.OPEN_CONTAINER()
                    return
            _DISPLAY = ""
            for ITEM in _LOCATION.LOCAL_ITEMS:
                _DISPLAY += f"\n{ITEM.NAME}: {ITEM.POSITION}"
            UPDATE_DISPLAY("INFO", DISPLAY["INFO"]+_DISPLAY)
        for MOB in MOBS:
            if MOB and LOCATION_ID(*MOB.POSITION[0:2]):
                PERCEPTION = ROLL(1,20) + self.WISDOM_MODIFIER + self.PROFICIENCY
                STEALTH = ROLL(1,20) + MOB.DEXTERITY_MODIFIER + MOB.PROFICIENCY
                logging.debug(f"PERCEPTION: {PERCEPTION} STEALTH: {STEALTH}")
                if PERCEPTION > STEALTH:
                    logging.debug("PERCEPTION successful.")
                    self.PERCEPTION_CHECK = True
                    MOB.SEEN = True


    def OPEN_INVENTORY(self):
        _DISPLAY = "\n"
        _DISPLAY += f"\nEXPERIENCE LEVEL: {self.EXPERIENCE_LEVEL}"
        _DISPLAY += f"\nEXPERIENCE POINTS: {self.EXPERIENCE}"
        _DISPLAY += "\nINVENTORY:"
        if self.INVENTORY["WEAPON"]:
            WEAPON = self.INVENTORY["WEAPON"]
            _DISPLAY += f"\n     WEAPON: {WEAPON.DESCRIPTION}"
            if "VERSATILE" in WEAPON.ATTRIBUTES:
                if WEAPON.SECOND_HAND:
                    _DISPLAY += " (BOTH HANDS)"
                else:
                    _DISPLAY += " (ONE HAND)"
            elif "TWO-HANDED" in WEAPON.ATTRIBUTES:
                _DISPLAY += " (BOTH HANDS)"
        else:
            _DISPLAY += f"\n     WEAPON: None."
        if self.INVENTORY["ARMOR"]:
            ARMOR = self.INVENTORY["ARMOR"].DESCRIPTION
        else:
            ARMOR = None
        _DISPLAY += f"\n     ARMOR: {ARMOR}"
        if self.INVENTORY["SHIELD"]:
            _DISPLAY += "\n     SHIELD"
        if self.INVENTORY["ARROWS"]:
            _DISPLAY += f"\n     ARROWS: {self.INVENTORY["ARROWS"]}"
        if self.INVENTORY["SLING-PELLETS"]:
            _DISPLAY += f"\n     SLING-PELLETS: {self.INVENTORY["SLING-PELLETS"]}"
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
            if NUM == "F":
                _ITEM = self.INVENTORY["WEAPON"]
                self.INVENTORY["WEAPON"] = None
            elif NUM == "G":
                _ITEM = self.INVENTORY["SHIELD"]
                self.INVENTORY["SHIELD"] = None
            else:
                _ITEM = _ITEMS.pop(NUM)
            if _ITEM:
                _ITEM.POSITION = self.POSITION[0:4]
                _ITEM.CHARACTER = "i"
                ROOM = LOCATION_ID(*self.POSITION[0:2])
                x = True
                m = ""
                if len(ROOM.LOCAL_ITEMS):
                    for ITEM in ROOM.LOCAL_ITEMS:
                        if ITEM in CONTAINERS and DISTANCE(*self.POSITION[0:2], *ITEM.POSITION[0:2]) < 2 and ITEM.OPEN and len(ITEM.CONTENTS) < 10:
                            ITEM.CONTENTS.append(_ITEM)
                            x = False
                            m = f" in {ITEM.NAME}"
                            break
                if x:
                    ROOM.ADD_ITEM(_ITEM)
                _DISPLAY = f"\nDROPPED {_ITEM.NAME}{m}."
                
                UPDATE_DISPLAY("INFO", _DISPLAY)

        except IndexError as e:
            logging.debug(f"IndexError: {e}")
            logging.debug(f"NUM: {NUM}\nITEMS:{_ITEMS}")
        

    
    def EQUIP_ITEM(self, NUM, V=False, HANDS=None):
        _ITEMS = self.INVENTORY["ITEMS"]
        _DISPLAY = None
        VERSATILE = False
        
        try:
            if NUM == "F":
                if len(_ITEMS)< 10 and self.INVENTORY["WEAPON"]:
                    logging.debug("EQUIPPING F.")
                    _ITEM = self.INVENTORY["WEAPON"]
                    _ITEMS.append(_ITEM)
                    self.INVENTORY["WEAPON"] = None
                    _DISPLAY = f"\nUNEQUIPPED {_ITEM.NAME}"
                else:
                    _DISPLAY = f"\nUNABLE TO UNEQUIP ITEM."
                    raise ValueError
            elif NUM == "G":
                if len(_ITEMS)< 10 and self.INVENTORY["SHIELD"]:
                    _ITEM = self.INVENTORY["SHIELD"]
                    _ITEMS.append(_ITEM)
                    self.INVENTORY["SHIELD"] = None
                    _DISPLAY = f"\n\nUNEQUIPPED {_ITEM.NAME}"
                else:
                    _DISPLAY = f"\n\nUNABLE TO UNEQUIP ITEM."
                    raise ValueError
            elif NUM == "H":
                if len(_ITEMS)< 10 and self.INVENTORY["ARMOR"]:
                    _ITEM = self.INVENTORY["ARMOR"]
                    self.INVENTORY["ARMOR"] = None
                    _ITEMS.append(_ITEM)
                    _DISPLAY = f"\n\nUNEQUIPPED {_ITEM.NAME}"
                else:
                    _DISPLAY = f"\n\nUNABLE TO UNEQUIP ITEM."
                    raise ValueError
            else:
                _ITEM = _ITEMS[NUM]
                logging.debug(self.INVENTORY["ITEMS"])
                logging.debug(NUM)
                if isinstance(_ITEM, MELEE_WEAPON) or isinstance(_ITEM, RANGED_WEAPON):
                    if "VERSATILE" in _ITEM.ATTRIBUTES and not V:
                        VERSATILE = True
                        _DISPLAY = f"\n\nTHIS WEAPON IS VERSATILE. ONE-HANDED OR TWO-HANDED?"
                    else:
                        if "TWO-HANDED" in _ITEM.ATTRIBUTES or HANDS == 2:
                            try:
                                if self.INVENTORY["SHIELD"]:
                                    self.EQUIP_ITEM("G")
                                _ITEM.SECOND_HAND = True
                            except ValueError:
                                _DISPLAY = f"\n\nUNABLE TO UNEQUIP SHIELD: INSUFFICIENT SPACE."
                                UPDATE_DISPLAY("INFO", _DISPLAY)
                                return
                        elif "VERSALTILE" in _ITEM.ATTRIBUTES:
                            _ITEM.DAMAGE = _ITEM.DAMAGE1
                                
                        _WEAPON = self.INVENTORY["WEAPON"]
                        if _WEAPON:
                            _ITEMS.append(_WEAPON)
                        self.INVENTORY["WEAPON"] = _ITEM
                        _ITEMS.remove(_ITEM)
                        _DISPLAY = f"\n\nEQUIPPED {_ITEM.NAME}"
                elif _ITEM.TYPE == "SHIELD":
                    _SHIELD = self.INVENTORY["SHIELD"]
                    _WEAPON = self.INVENTORY["WEAPON"]
                    if _WEAPON:
                        if "TWO-HANDED" in _WEAPON.ATTRIBUTES:
                            _DISPLAY = f"\n\nCANNOT EQUIP SHIELD. WEAPON IS TWO-HANDED."
                            UPDATE_DISPLAY("INFO", _DISPLAY)
                            return
                        elif _WEAPON.SECOND_HAND:
                            _WEAPON.SECOND_HAND = False
                            _WEAPON.DAMAGE = _WEAPON.DAMAGE1
                    if _SHIELD:
                        _ITEMS.append(_SHIELD)
                    self.INVENTORY["SHIELD"] = _ITEM
                    _ITEMS.remove(_ITEM)
                    _DISPLAY = f"\n\nEQUIPPED {_ITEM.NAME}"
                elif isinstance(_ITEM, ARMOR):
                    _ARMOR = self.INVENTORY["ARMOR"]
                    if _ARMOR:
                        self.INVENTORY["ITEMS"].append(_ARMOR)
                    self.INVENTORY["ITEMS"].remove(_ITEM)
                    self.INVENTORY["ARMOR"] = _ITEM
                    _DISPLAY = f"\n\nEQUIPPED {_ITEM.NAME}"
            
            logging.debug("UPDATING DISPLAY.")
            if _DISPLAY:
                UPDATE_DISPLAY("INFO", _DISPLAY)
            if VERSATILE:
                return "VERSATILE"

        except IndexError as e:
            logging.debug(f"IndexError: {e}")
            logging.debug(f"NUM: {NUM}\nITEMS:{_ITEMS}")
        
    
    def LOOT(self):
        _LOCATION = LOCATION_ID(*self.POSITION[0:2])
        if len(_LOCATION.LOCAL_ITEMS):
            for ITEM in _LOCATION.LOCAL_ITEMS:
                if len(self.INVENTORY["ITEMS"]) >= 10:
                    break
                if ITEM not in CONTAINERS and DISTANCE(*self.POSITION[0:2], *ITEM.POSITION[0:2]) < 2:
                    self.INVENTORY["ITEMS"].append(ITEM)
                    ITEM.POSITION = None
                    _LOCATION.REMOVE_ITEM(ITEM)
                    return
            for ITEM in _LOCATION.LOCAL_ITEMS:
                if ITEM in CONTAINERS and DISTANCE(*self.POSITION[0:2], *ITEM.POSITION[0:2]) < 2 and ITEM.OPEN:
                    if ITEM.GOLD:
                        self.INVENTORY["GOLD"] += ITEM.GOLD
                        ITEM.GOLD = 0
                    if ITEM.ARROWS:
                        self.INVENTORY["ARROWS"] += ITEM.ARROWS
                        ITEM.ARROWS = 0
                    if ITEM.SLING_PELLETS:
                        self.INVENTORY["SLING-PELLETS"] += ITEM.SLING_PELLETS
                        ITEM.SLING_PELLETS = 0
                    if ITEM.WATER:
                        self.INVENTORY["WATER"] += ITEM.WATER
                        ITEM.WATER = 0
                    while len(ITEM.CONTENTS) and len(self.INVENTORY["ITEMS"]) < 10:
                        _ITEM = ITEM.CONTENTS[0]
                        self.INVENTORY["ITEMS"].append(_ITEM)
                        ITEM.REMOVE_ITEM(_ITEM)
                    ITEM.VIEW_CONTENTS()
                    return
    

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
    

    def SELECT_MOB(self, MODE):
        if MODE == "RANGED":
            SIGHT = SORT_MOBS(self)
        if MODE == "MELEE":
            WEAPON = self.INVENTORY["WEAPON"]
            REACH = False
            if WEAPON and "REACH" in WEAPON.ATTRIBUTES:
                REACH = True
            SIGHT = SORT_MOBS_MELEE(self, REACH)
        _DISPLAY = "\nSelect Target:"
        for i in range(len(SIGHT)):
            _DISPLAY += f"\n{i}: {SIGHT[i].NAME}"
        UPDATE_DISPLAY("INFO", _DISPLAY)

    
    def DRINK(self):
        WATER = self.INVENTORY["WATER"]
        if WATER:
            WATER -= 1
            self.WATER = min(self.MAX_WATER, self.WATER+1)

    
    def SELECT_REST(self):
        _DISPLAY = ""
        TIME = GLOBAL_FLAGS["TIME"]
        if TIME - self.LONG_REST > 86400:
            _DISPLAY += "\n0. LONG REST: 8 HOURS."
        _DISPLAY += "\n1. SHORT REST: 1 HOUR."
        UPDATE_DISPLAY("INFO", _DISPLAY)


    def VERSATILE(self, NUM):
        if len(self.INVENTORY["ITEMS"]) > NUM and "VERSATILE" in self.INVENTORY["ITEMS"][NUM].ATTRIBUTES:
            return True
        return False