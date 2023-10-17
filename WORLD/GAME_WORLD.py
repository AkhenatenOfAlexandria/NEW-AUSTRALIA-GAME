from WORLD.LOCATION import LOCATION

infinity = float('inf')

CENTRAL_ROOM = LOCATION(-3, 3, 3, -3, "SMALL ROOM", DOORS={
        "NORTH" : (-3, 0),
        "SOUTH": (3, 0),
        "WEST": (0, -3)
        }
    )
SOUTH_CORRIDOR = LOCATION(4, 31, 3, -3, "CORRIDOR", DOORS={"NORTH":(3, 0)})
NORTH_CORRIDOR = LOCATION(-31, -4, 3, -3, "CORRIDOR", DOORS={"SOUTH":(-3, 0)})
WEST_CORRIDOR = LOCATION(-3, 3, -4, -31, "CORRIDOR", DOORS={"EAST":(0, -3), "WEST": (0, -31)})
VICTORY = LOCATION(-infinity, infinity, -31, -infinity, "Level complete!")

GAME_WORLD = [
    CENTRAL_ROOM,
    SOUTH_CORRIDOR,
    NORTH_CORRIDOR,
    WEST_CORRIDOR,
    VICTORY
]
