from LOCATION import LOCATION

SMALL_ROOM1 = LOCATION(-3, 3, 3, -3, "You are in a small room."),
CORRIDOR1 = LOCATION(-15, 4, 3, -3, "You are in a corridor."),
CORRIDOR2 = LOCATION(4, 15, 3, -3, "You are in a corridor."),
CORRIDOR3 = LOCATION(-3, 3, -15, 4, "You are in a corridor.")

GAME_WORLD = [
    SMALL_ROOM1,
    CORRIDOR1,
    CORRIDOR2,
    CORRIDOR3
]
