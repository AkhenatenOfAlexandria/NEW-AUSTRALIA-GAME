from __future__ import annotations
from WORLD.GLOBAL import PLAYERS, MOBS, DISPLAY, GLOBAL_FLAGS, UPDATE_DISPLAY, UPDATE_FLAG
from WORLD.SPAWN import PLAYER_SPAWN
from WORLD.HEADS_UP_DISPLAY import INITIALIZE_DISPLAY
from WORLD.GAME_WORLD import GAME_WORLD
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID

import attr
import tcod.console
import tcod.event

@attr.s
class GAMESTATE:
    PLAYER_COUNT = 1
    PLAYER_SPAWN(PLAYER_COUNT)
    INITIALIZE_DISPLAY()
    

    def ON_DRAW(self, CONSOLE: tcod.console.Console) -> None:
        PLAYER = PLAYERS[0]
        if not PLAYER:
            CONSOLE.print(CONSOLE.width//2, CONSOLE.height//2, "GAME OVER")
            return
        LEVEL = GLOBAL_FLAGS["LEVEL"]
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
        match EVENT:
            case tcod.event.Quit():
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
                UPDATE_DISPLAY("INFO", "")

    
    def UPDATE(self, MOVE):
        UPDATE_FLAG("TIME", GLOBAL_FLAGS["TIME"]+1)
        PLAYER = PLAYERS[0]
        if not PLAYER:
            return
        for MOB in MOBS:
            if MOB and LOCATION_ID(*MOB.POSITION[0:2]) == LOCATION_ID(*PLAYER.POSITION[0:2]):
                MOB.UPDATE(MOVE)
