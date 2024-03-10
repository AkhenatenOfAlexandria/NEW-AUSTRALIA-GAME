from __future__ import annotations
from WORLD.GLOBAL import PLAYERS, MOBS, DISPLAY, GLOBAL_FLAGS, UPDATE_DISPLAY, UPDATE_FLAG
from WORLD.SPAWN import PLAYER_SPAWN
from WORLD.HEADS_UP_DISPLAY import INITIALIZE_DISPLAY
from WORLD.GAME_WORLD import GAME_WORLD
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID

import attr
import tcod.console
import tcod.event

Q_ACTIVE = False
E_ACTIVE = False

@attr.s
class GAMESTATE:
    PLAYER_COUNT = 1
    PLAYER_SPAWN(PLAYER_COUNT)
    INITIALIZE_DISPLAY()
    

    def ON_DRAW(self, CONSOLE: tcod.console.Console) -> None:
        LEVEL = GLOBAL_FLAGS["LEVEL"]
        PLAYER = PLAYERS[0]
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
        _MOVE = None
        match EVENT:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                raise SystemExit()
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
            case tcod.event.KeyDown(sym=tcod.event.KeySym.i):
                PLAYER.OPEN_INVENTORY()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.BACKSPACE):
                E_ACTIVE = False
                Q_ACTIVE = False
                UPDATE_DISPLAY("INFO", "\n")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.l):
                self.UPDATE("LOOT")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.r):
                self.UPDATE("LONG REST")
            case tcod.event.KeyDown(sym=tcod.event.KeySym.q):
                if E_ACTIVE:
                    UPDATE_DISPLAY("INFO", f"\n\nEQUIP CANCELLED.")
                    E_ACTIVE = False
                if Q_ACTIVE:
                    UPDATE_DISPLAY("INFO", f"\n\nDROP CANCELLED.")
                    Q_ACTIVE = False
                else:
                    PLAYER.SELECT_ITEM()
                    Q_ACTIVE = True
            case tcod.event.KeyDown(sym=tcod.event.KeySym.e):
                if Q_ACTIVE:
                    UPDATE_DISPLAY("INFO", f"\n\nDROP CANCELLED.")
                    Q_ACTIVE = False
                if E_ACTIVE:
                    UPDATE_DISPLAY("INFO", f"\n\nEQUIP CANCELLED.")
                    E_ACTIVE = False
                else:
                    PLAYER.SELECT_ITEM()
                    E_ACTIVE = True
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N0):
                _NUM = 0
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N1):
                _NUM = 1
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N2):
                _NUM = 2
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N3):
                _NUM = 3
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N4):
                _NUM = 4
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N5):
                _NUM = 5
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N6):
                _NUM = 6
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N7):
                _NUM = 7
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N8):
                _NUM = 8
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N9):
                _NUM = 9
                if Q_ACTIVE:
                    _MOVE = "DROP"
                    Q_ACTIVE = False
                if E_ACTIVE:
                    _MOVE = "EQUIP"
                    E_ACTIVE = False
                if _MOVE is not None and len(PLAYER.INVENTORY["ITEMS"]) > _NUM:
                    self.UPDATE(_MOVE, _NUM)

    
    def UPDATE(self, MOVE, NUM=None):
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        UPDATE_FLAG("TIME", GLOBAL_FLAGS["TIME"]+1)
        _REST = True
        for MOB in MOBS:
            if MOB and LOCATION_ID(*MOB.POSITION[0:2]) == LOCATION_ID(*PLAYER.POSITION[0:2]):
                MOB.UPDATE(MOVE, NUM)
                if MOB != PLAYER:
                    _REST = False
        if MOVE == "LONG REST" and _REST:
            PLAYER.HEALTH = PLAYER.MAX_HEALTH
