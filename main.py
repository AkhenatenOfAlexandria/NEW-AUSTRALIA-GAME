from __future__ import annotations

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset

from GAMESTATE import GAMESTATE
from WORLD.GLOBAL import GLOBAL_FLAGS, UPDATE_FLAG, PLAYERS, UPDATE_DISPLAY
from WORLD.GAME_WORLD import CREATE_LEVEL, GAME_WORLD
from WORLD.SPAWN import SPAWN
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID


def MAIN():
	VERSION = "ALPHA 1.0.1"
	
	WIDTH = 72
	HEIGHT = 58

	tileset = tcod.tileset.load_tilesheet(
			"Alloy_curses_12x12.png", columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
		)

	tcod.tileset.procedural_block_elements(tileset=tileset)

	CONSOLE = tcod.console.Console(WIDTH, HEIGHT)
	STATE = GAMESTATE()
	PLAYER = PLAYERS[0]

	with tcod.context.new(columns = WIDTH, rows = HEIGHT, tileset=tileset) as context:
		GAME_RUNNING = True
		while GAME_RUNNING:
			LEVEL = GLOBAL_FLAGS["LEVEL"]
			LEVEL = UPDATE_FLAG("LEVEL", LEVEL+1)
			if LEVEL > 1:
				CREATE_LEVEL()
			else:
				for ROOM in GAME_WORLD[LEVEL]:
					ROOM.STRING = ROOM._DRAW()

			SPAWN()

			UPDATE_DISPLAY("INFO", "\n")

			while GAME_RUNNING:
				CONSOLE.clear()
				_LOCATION = LOCATION_ID(*PLAYER.POSITION[0:2])
				if _LOCATION:
					_LOCATION.FOUND = True
				STATE.ON_DRAW(CONSOLE)
				context.present(CONSOLE)
				for event in tcod.event.wait():
					print(event)
					STATE.ON_EVENT(event)
				if not PLAYER:
					GAME_RUNNING = False
				elif GLOBAL_FLAGS["NEW LEVEL"]:
					UPDATE_FLAG("NEW LEVEL", False)
					break


if __name__ == "__main__":
	MAIN()
