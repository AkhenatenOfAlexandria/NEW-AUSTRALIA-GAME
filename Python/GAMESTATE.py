from __future__ import annotations
from WORLD.GLOBAL import PLAYERS, MOBS, DISPLAY, GLOBAL_FLAGS, UPDATE_DISPLAY, UPDATE_FLAG
from WORLD.SPAWN import PLAYER_SPAWN
from WORLD.HEADS_UP_DISPLAY import INITIALIZE_DISPLAY
from WORLD.GAME_WORLD import GAME_WORLD
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID
from LOGIC.MATH import ROLL

import attr
import tcod.console
import tcod.event
import logging
import math

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

Q_ACTIVE = False
E_ACTIVE = False
VERSATILE = False
CACHE = None
Z_ACTIVE = False
X_ACTIVE = False
I_ACTIVE = False
R_ACTIVE = False

@attr.s
class GAMESTATE:
    PLAYER_COUNT = 1
    PLAYER_SPAWN(PLAYER_COUNT)
    INITIALIZE_DISPLAY()
    

    def ON_DRAW(self, CONSOLE: tcod.console.Console) -> None:
        LEVEL = GLOBAL_FLAGS["LEVEL"]
        PLAYER = PLAYERS[0]
        if LEVEL > 25:
            SCORE, GOLD = GLOBAL_FLAGS["SCORE"], GLOBAL_FLAGS["GOLD"]
            CONSOLE.print((CONSOLE.width//2)-5, (CONSOLE.height//2)-5, f"GAME OVER\nYOU WIN!\nSCORE: {SCORE}\nGOLD: {GOLD}")
            return
        if not PLAYER:
            SCORE, GOLD = GLOBAL_FLAGS["SCORE"], GLOBAL_FLAGS["GOLD"]
            CONSOLE.print((CONSOLE.width//2)-5, (CONSOLE.height//2)-5, f"GAME OVER\nLEVEL: {LEVEL}\nSCORE: {SCORE}\nGOLD: {GOLD}")
            return
        for ROOM in GAME_WORLD[LEVEL]:
            if ROOM and ROOM.FOUND:
                ROOM.DRAW(CONSOLE)
        for MOB in MOBS:
            if MOB and MOB not in PLAYERS and LOCATION_ID(*PLAYER.POSITION[0:2]) == LOCATION_ID(*MOB.POSITION[0:2]):
                MOB.DRAW(CONSOLE)
        for PLAYER in PLAYERS:
                PLAYER.DRAW(CONSOLE)
        HUD = DISPLAY["HUD"]
        
        HUD.DRAW(CONSOLE)


    def ON_EVENT(self, EVENT):
        PLAYER = PLAYERS[0]
        global Q_ACTIVE
        global E_ACTIVE
        global VERSATILE
        global CACHE
        global Z_ACTIVE
        global X_ACTIVE
        global I_ACTIVE
        global R_ACTIVE
        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
        _MOVE = None
        match EVENT:
            case tcod.event.Quit():
                raise SystemExit()
                '''case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                    raise SystemExit()'''
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N0):
                _NUM = 0
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 0
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if R_ACTIVE:
                    _MOVE = "LONG REST"
                    R_ACTIVE = False
                    UPDATE_DISPLAY("INFO", f"")
                    self.UPDATE(_MOVE)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N1):
                _NUM = 1
                logging.debug(f"1 PRESSED. VERSATILE: {VERSATILE}")
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 1
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if R_ACTIVE:
                    _MOVE = "SHORT REST"
                    R_ACTIVE = False
                    UPDATE_DISPLAY("INFO", f"")
                    self.UPDATE(_MOVE)
                if (_MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM) or VERSATILE:
                    if VERSATILE:
                        logging.debug("Attempting to equip VERSATILE weapon.")
                        self.UPDATE("EQUIP", CACHE, VERSATILE, _NUM)
                        VERSATILE = False
                    elif self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 1
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N2):
                _NUM = 2
                logging.debug(f"2 PRESSED. VERSATILE: {VERSATILE}")
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 2
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if (_MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM) or VERSATILE:
                    if VERSATILE:
                        logging.debug("Attempting to equip VERSATILE weapon.")
                        self.UPDATE("EQUIP", CACHE, VERSATILE, _NUM)
                        VERSATILE = False
                    elif self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 2
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N3):
                _NUM = 3
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 3
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 3
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N4):
                _NUM = 4
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 4
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 4
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N5):
                _NUM = 5
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 5
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 5
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N6):
                _NUM = 6
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 6
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 6
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N7):
                _NUM = 7
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 7
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 7
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N8):
                _NUM = 8
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 8
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 8
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N9):
                _NUM = 9
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    if PLAYER.VERSATILE(_NUM):
                        PLAYER.UPDATE(_MOVE, _NUM)
                        VERSATILE = True
                        CACHE = 9
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
                        _MOVE = None
                    E_ACTIVE = False
                if Z_ACTIVE:
                    _MOVE = "RANGED_ATTACK"
                    Z_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                if X_ACTIVE:
                    _MOVE = "MELEE_ATTACK"
                    X_ACTIVE = False
                    self.UPDATE(_MOVE, _NUM)
                elif _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    if self.UPDATE(_MOVE, _NUM):
                        VERSATILE = True
                        CACHE = 9
                        logging.debug(f"VERSATILE: {VERSATILE}; CACHE: {CACHE}")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                self.UPDATE("LEFT")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.a):
                self.UPDATE("LEFT")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                self.UPDATE("RIGHT")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.d):
                self.UPDATE("RIGHT")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                self.UPDATE("UP")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.w):
                self.UPDATE("UP")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                self.UPDATE("DOWN")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.s):
                self.UPDATE("DOWN")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.SPACE):
                self.UPDATE("SPACE")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.BACKSPACE):
                E_ACTIVE = False
                Q_ACTIVE = False
                I_ACTIVE = False
                X_ACTIVE = False
                Z_ACTIVE = False
                VERSATILE = False
                UPDATE_DISPLAY("INFO", "\n")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.e):
                logging.debug("E PRESSED.")
                if Q_ACTIVE:
                    UPDATE_DISPLAY("INFO", f"\n\nDROP CANCELLED.")
                    Q_ACTIVE = False
                if E_ACTIVE or VERSATILE:
                    UPDATE_DISPLAY("INFO", f"\n\nEQUIP CANCELLED.")
                    E_ACTIVE = False
                    VERSATILE = False
                else:
                    PLAYER.SELECT_ITEM()
                    E_ACTIVE = True
            case tcod.event.KeyDown(sym=tcod.event.KeySym.f):
                logging.debug("F PRESSED.")
                _NUM = "F"
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                    logging.debug("ATTEMPTED TO EQUIP F.")
                if _MOVE:
                    logging.debug("ATTEMPTING TO EQUIP F.")
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.g):
                _NUM = "G"
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.i):
                E_ACTIVE = False
                Q_ACTIVE = False
                X_ACTIVE = False
                Z_ACTIVE = False
                VERSATILE = False
                if I_ACTIVE:
                    I_ACTIVE = False
                    UPDATE_DISPLAY("INFO", "\n")
                else:
                    I_ACTIVE = True
                    PLAYER.OPEN_INVENTORY()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.l):
                self.UPDATE("LOOT")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.q):
                if E_ACTIVE or VERSATILE:
                    UPDATE_DISPLAY("INFO", f"\n\nEQUIP CANCELLED.")
                    E_ACTIVE = False
                    VERSATILE = False
                if Q_ACTIVE:
                    UPDATE_DISPLAY("INFO", f"\n\nDROP CANCELLED.")
                    Q_ACTIVE = False
                else:
                    PLAYER.SELECT_ITEM()
                    Q_ACTIVE = True
            case tcod.event.KeyDown(sym=tcod.event.KeySym.r):
                I_ACTIVE = False
                if Z_ACTIVE or X_ACTIVE or Q_ACTIVE or E_ACTIVE:
                    pass
                elif R_ACTIVE:
                    R_ACTIVE = False
                    UPDATE_DISPLAY("INFO", f"\nREST CANCELLED.")
                else:
                    R_ACTIVE = True
                    PLAYER.SELECT_REST()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.v):
                if PLAYER.INVENTORY["WATER"]:
                    self.UPDATE("DRINK")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.x):
                WEAPON = PLAYER.INVENTORY["WEAPON"]
                Z_ACTIVE = False
                if Q_ACTIVE or E_ACTIVE or VERSATILE:
                    pass
                elif X_ACTIVE:
                    X_ACTIVE = False
                    UPDATE_DISPLAY("INFO", f"\n\nATTACK CANCELLED.")
                else:
                    X_ACTIVE = True
                    PLAYER.SELECT_MOB("MELEE")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.z):
                WEAPON = PLAYER.INVENTORY["WEAPON"]
                X_ACTIVE = False
                if Q_ACTIVE or E_ACTIVE or VERSATILE:
                    pass
                elif Z_ACTIVE:
                    Z_ACTIVE = False
                    UPDATE_DISPLAY("INFO", f"\n\nATTACK CANCELLED.")
                elif WEAPON and ("RANGED" in WEAPON.ATTRIBUTES or "THROWN" in WEAPON.ATTRIBUTES):
                    Z_ACTIVE = True
                    PLAYER.SELECT_MOB("RANGED")

    
    def UPDATE(self, MOVE, NUM=None, V=False, HANDS=None):
        TIME = GLOBAL_FLAGS["TIME"]
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        UPDATE_FLAG("TIME", GLOBAL_FLAGS["TIME"]+1)
        _REST = True
        versatile = False
        for MOB in MOBS:
            if MOB and LOCATION_ID(*MOB.POSITION[0:2]) == LOCATION_ID(*PLAYER.POSITION[0:2]):
                if MOB.UPDATE(MOVE, NUM, V, HANDS):
                    versatile = True
                if MOB != PLAYER:
                    _REST = False
        if MOVE == "LONG REST" and _REST and TIME-PLAYER.LONG_REST > 86400:
            _TIME = 0
            PLAYER.LONG_REST = int(TIME)
            while _TIME < 28800:
                self.UPDATE("")
                _TIME += 1
            if PLAYER.EXHAUSTION < 4:
                PLAYER.HEALTH = max(PLAYER.HEALTH, PLAYER.MAX_HEALTH)
            else:
                PLAYER.HEALTH = max(PLAYER.HEALTH, int(PLAYER.MAX_HEALTH/2))
            if PLAYER.WATER:
                PLAYER.EXHAUSTION = max(0, PLAYER.EXHAUSTION-1)
            PLAYER.HIT_DICE = min(
                PLAYER.MAX_HIT_DICE,
                PLAYER.HIT_DICE + max (
                    int(PLAYER.MAX_HIT_DICE/2), 1 ))
        if MOVE == "SHORT REST" and _REST:
            _TIME = 0
            while _TIME < 3600:
                self.UPDATE("")
                _TIME += 1
            while PLAYER.HIT_DICE and PLAYER.MAX_HEALTH-PLAYER.HEALTH:
                PLAYER.HEALTH = min(PLAYER.HEALTH+ROLL(1,10)+PLAYER.CONSTITUTION_MODIFIER, PLAYER.MAX_HEALTH)
                PLAYER.HIT_DICE -= 1
        if versatile:
            return "VERSATILE"
