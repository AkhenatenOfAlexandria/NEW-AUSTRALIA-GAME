
def PROCESS_COMMAND(PLAYER, MOBS):
    POSITION = PLAYER.POSITION
    PROMPT = True
    while True:  # Keep looping until a valid command is entered
        COMMAND = input("\nEnter your COMMAND: ").upper()  # Ask for a new command
        if COMMAND == "QUIT":
            return False, POSITION

        elif COMMAND.startswith(("NORTH", "SOUTH", "EAST", "WEST")):
            PARTS = COMMAND.split()
            DIRECTION = PARTS[0]
            if PLAYER.ROOM_CHECK(MOBS):
                DISTANCE = 1
            elif len(PARTS) > 1:
                DISTANCE = int(PARTS[1])
            else:
                DISTANCE = 1

            POSITION = PLAYER.MOVE(DIRECTION, DISTANCE)
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
            print(f"EXPERIENCE LEVEL: {PLAYER.EXPERIENCE_LEVEL}")
            print(f"EXPERIENCE POINTS: {PLAYER.EXPERIENCE}")
            print("INVENTORY:")
            if PLAYER.INVENTORY["WEAPON"]:
                WEAPON = PLAYER.INVENTORY["WEAPON"].NAME
            else:
                WEAPON = None
            if PLAYER.INVENTORY["ARMOR"]:
                ARMOR = PLAYER.INVENTORY["ARMOR"].NAME
            else:
                ARMOR = None
            print(f"\tWEAPON: {WEAPON}")
            print(f"\tARMOR: {ARMOR}")
            if PLAYER.INVENTORY["SHIELD"]:
                print("\tSHIELD")
            print(f"\tGOLD: {PLAYER.INVENTORY['GOLD']}")
            print(f'\tITEMS: {PLAYER.INVENTORY["ITEMS"]}')

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
