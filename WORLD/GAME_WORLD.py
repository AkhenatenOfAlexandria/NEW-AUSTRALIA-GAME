from WORLD.LOCATION import LOCATION

infinity = float('inf')

CENTRAL_ROOM = LOCATION(-3, 3, 3, -3, "You are in a small room.", DOORS={
        "NORTH" : (3, 0),
        "SOUTH": (-3, 0),
        "WEST": (0, -3)
        }
    )
SOUTH_CORRIDOR = LOCATION(-15, -4, 3, -3, "You are in a corridor.", DOORS={"NORTH":(-3, 0)})
NORTH_CORRIDOR = LOCATION(4, 15, 3, -3, "You are in a corridor.", DOORS={"SOUTH":(3, 0)})
WEST_CORRIDOR = LOCATION(-3, 3, -4, -15, "You are in a corridor.", DOORS={"EAST":(0, -3), "WEST": (0, -15)})
VICTORY = LOCATION(-infinity, infinity, -15, -infinity, "Level complete!")

GAME_WORLD = [
    CENTRAL_ROOM,
    SOUTH_CORRIDOR,
    NORTH_CORRIDOR,
    WEST_CORRIDOR
]
