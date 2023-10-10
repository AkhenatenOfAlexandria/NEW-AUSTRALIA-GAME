from LOGIC.LOCATION_ID import LOCATION_ID


def PROCESS_COMMAND(COMMAND, PLAYER, MOBS):
    POSITION = PLAYER.POSITION
    if COMMAND.upper() == "QUIT":
        return False, POSITION

    elif COMMAND.upper().startswith(("NORTH", "SOUTH", "EAST", "WEST")):
        PARTS = COMMAND.split()
        DIRECTION = PARTS[0].upper()
        '''DISTANCE = int(PARTS[1]) if len(PARTS) > 1\
            else 1'''
        DISTANCE = 1
        POSITION = PLAYER.MOVE(DIRECTION, DISTANCE)
        if POSITION == PLAYER.POSITION:
            print("There is a wall in your path.")
        CURRENT_LOCATION = LOCATION_ID(*POSITION)

    elif COMMAND.upper() == "LOOK":
        pass

    elif COMMAND.upper() == "ATTACK":
        TARGET_ID = int(input("Select TARGET: "))
        if MOBS[TARGET_ID]:
            TARGET = MOBS[TARGET_ID]
            if TARGET == PLAYER:
                print("You cannot attack yourself.")
            elif TARGET.POSITION != POSITION:
                print("TARGET is too far away.")
            else:
                ATTACK, GAME_RUNNING = PLAYER.COMBAT_CHECK(TARGET, MOBS)
                return GAME_RUNNING, POSITION
        else:
            print("Invalid TARGET")
    else:
        print("Invalid COMMAND. Try again.")

    return True, POSITION
