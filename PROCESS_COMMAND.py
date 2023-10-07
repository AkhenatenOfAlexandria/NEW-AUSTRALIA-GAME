from MOVE_ENTITY import MOVE_ENTITY
from PLAYER_LOCATION import PLAYER_LOCATION


def PROCESS_COMMAND(COMMAND, PLAYER_POSITION):
    if COMMAND == "QUIT":
        return False, PLAYER_POSITION

    if COMMAND.startswith(("NORTH", "SOUTH", "EAST", "WEST")):
        PARTS = COMMAND.split()
        DIRECTION = PARTS[0]
        DISTANCE = int(PARTS[1]) if len(PARTS) > 1\
            else 1
        PLAYER_POSITION = MOVE_ENTITY(PLAYER_POSITION, DIRECTION, DISTANCE)
        print(f"{PLAYER_POSITION}: {PLAYER_LOCATION(*PLAYER_POSITION)}")

    elif COMMAND == "LOOK":
        print(f"{PLAYER_POSITION}: {PLAYER_LOCATION(*PLAYER_POSITION)}")

    else:
        print("Invalid COMMAND. Try again.")

    return True, PLAYER_POSITION
