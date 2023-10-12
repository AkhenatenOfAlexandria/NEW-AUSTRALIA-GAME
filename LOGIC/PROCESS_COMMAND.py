
def PROCESS_COMMAND(PLAYER, MOBS):
    POSITION = PLAYER.POSITION
    PROMPT = True
    while True:  # Keep looping until a valid command is entered
        COMMAND = input("Enter your COMMAND: ").upper()  # Ask for a new command
        if COMMAND == "QUIT":
            return False, POSITION

        elif COMMAND in ("NORTH", "SOUTH", "EAST", "WEST"):
            DIRECTION = COMMAND
            POSITION = PLAYER.MOVE(DIRECTION)
            if POSITION == PLAYER.POSITION:
                print("There is a wall in your path.")
            else:
                print(f"Moved {DIRECTION}.")
                for mob in MOBS:
                    if mob != PLAYER and PLAYER.POSITION == mob.POSITION:
                        x, GAME_RUNNING = mob.COMBAT_CHECK(PLAYER, MOBS)
                        if not GAME_RUNNING:
                            return False, POSITION
                return True, POSITION

        elif COMMAND == "LOOK":
            return True, POSITION
        
        elif COMMAND == "INVENTORY":
            _INVENTORY = "INVENTORY: "
            print(f"INVENTORY: {PLAYER.INVENTORY}")

        elif COMMAND == "ATTACK":
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
                        return GAME_RUNNING, POSITION
                else:
                    print("Invalid TARGET. Enter the ID of the mob you want to attack.")
            except ValueError:
                print("Invalid TARGET. Enter the ID of the mob you want to attack.")

        elif COMMAND == "HELP":
            print("The objective is to escape the dungeon without being killed by the monsters.")
            print("To move, enter NORTH, SOUTH, EAST, or WEST.")
            print("To pass, enter LOOK.")
            print("To check inventory, enter INVENTORY.")
            print("To attack a monster, enter ATTACK.")
            print("To exit the game, enter QUIT.")
            print("For help, enter HELP.")

        else:
            print("Invalid COMMAND. Try again.")
