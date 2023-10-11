
def PROCESS_COMMAND(PLAYER, MOBS):
    POSITION = PLAYER.POSITION
    PROMPT = True
    while PROMPT:  # Keep looping until a valid command is entered
        COMMAND = input("Enter your COMMAND: ")  # Ask for a new command
        if COMMAND.upper() == "QUIT":
            PROMPT = False
            return False, POSITION

        elif COMMAND.upper().startswith(("NORTH", "SOUTH", "EAST", "WEST")):
            PARTS = COMMAND.split()
            DIRECTION = PARTS[0].upper()
            DISTANCE = 1
            POSITION = PLAYER.MOVE(DIRECTION, DISTANCE)
            if POSITION == PLAYER.POSITION:
                print("There is a wall in your path.")
            else:
                for mob in MOBS:
                    if mob != PLAYER and PLAYER.POSITION == mob.POSITION:
                        mob.COMBAT_CHECK(PLAYER, MOBS)
                PROMPT = False

        elif COMMAND.upper() == "LOOK":
            PROMPT = False

        elif COMMAND.upper() == "ATTACK":
            try:
                TARGET_ID = int(input("Select TARGET: "))
                if 0 <= TARGET_ID < len(MOBS):
                    TARGET = MOBS[TARGET_ID]
                    if TARGET == PLAYER:
                        print("You cannot attack yourself.")
                    elif TARGET.POSITION != POSITION:
                        print("TARGET is too far away.")
                    else:
                        ATTACK, GAME_RUNNING = PLAYER.COMBAT_CHECK(TARGET, MOBS)
                        PROMPT = False
                        return GAME_RUNNING, POSITION
                else:
                    print("Invalid TARGET. Enter the ID of the mob you want to attack.")
            except ValueError:
                print("Invalid TARGET. Enter the ID of the mob you want to attack.")

        elif COMMAND.upper() == "HELP":
            print("The objective is to escape the dungeon without being killed by the monsters.")
            print("To move, enter NORTH, SOUTH, EAST, or WEST.")
            print("To pass, enter LOOK.")
            print("To attack a monster, enter ATTACK.")
            print("To exit the game, enter QUIT.")
            print("For help, enter HELP.")

        else:
            print("Invalid COMMAND. Try again.")

    return True, POSITION
