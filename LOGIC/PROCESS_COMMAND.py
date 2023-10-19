from WORLD.GLOBAL_LISTS import MOBS, ITEMS
from ENTITIES.ITEMS.MELEE_WEAPON import MELEE_WEAPON
from LOGIC.MATH import MELEE_RANGE


def MOVE_PLAYER(PLAYER, COMMAND):
    PARTS = COMMAND.split()
    try:
        DIRECTION = PARTS[0]
        if len(PARTS) > 1:
            DISTANCE = int(PARTS[1])
            # print(DISTANCE)
            if DISTANCE % 5 == 0:    
                DISTANCE = int(DISTANCE/5)
                # print(DISTANCE)
                if PLAYER.ROOM_CHECK():
                    DISTANCE = min(DISTANCE, PLAYER.SPEED)
                    # print(DISTANCE)
            else:
                print("Invalid DISTANCE. DISTANCE must be divisible by 5.")
                return None
        else:
            DISTANCE = 1

        POSITION = PLAYER.MOVE(DIRECTION, DISTANCE)
        if POSITION == PLAYER.POSITION:
            print("There is a wall in your path.")
        else:
            print(f"Moved {DISTANCE*5} feet {DIRECTION}.")
            TEMP_X, TEMP_Y = PLAYER.POSITION
            NEW_X, NEW_Y = POSITION
            if TEMP_X == NEW_X:
                COORDINATE = 1
                _RANGE = abs(NEW_Y - TEMP_Y)
            else:
                COORDINATE = 0
                _RANGE = abs(NEW_X - TEMP_X)
            
            TEMP_POSITION = [TEMP_X, TEMP_Y]
            
            MOB_CHECKS = []

            if DIRECTION in ["NORTH", "WEST"]:
                CHANGE = -1
            else:
                CHANGE = 1

            for mob in MOBS:
                MOB_CHECKS.append(False)

            for i in range(_RANGE):
                for index, mob in enumerate(MOBS):
                    CHECK1 = MOB_CHECKS[index]
                    if mob and mob != PLAYER and MELEE_RANGE(*mob.POSITION, *TEMP_POSITION):
                        MOB_CHECKS[index] = True
                    else:
                        MOB_CHECKS[index] = False
                    CHECK2 = MOB_CHECKS[index]

                    if CHECK1 and not CHECK2:
                        x, GAME_RUNNING = mob.COMBAT_CHECK(PLAYER)
                        if not GAME_RUNNING:
                            return False, POSITION
                TEMP_POSITION[COORDINATE] += CHANGE
            return True, POSITION
    except ValueError:
        print("Invalid DISTANCE.")


def OPEN_INVENTORY(PLAYER):
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
    
    ITEMS = []

    for ITEM in PLAYER.INVENTORY["ITEMS"]:
        ITEMS.append(ITEM.NAME)
    
    print(f'\tITEMS: {ITEMS}')


def ATTACK(PLAYER, COMMAND):
    POSITION = PLAYER.POSITION
    PARTS = COMMAND.split()
    try:
        TARGET_ID = int(PARTS[1])-1
        if 0 < TARGET_ID < len(MOBS):
            TARGET = MOBS[TARGET_ID]
            if not TARGET:
                print("Invalid TARGET. Enter the ID of the mob you want to attack.")    
            elif TARGET == PLAYER:
                print("You cannot attack yourself.")
            elif MELEE_RANGE(*PLAYER.POSITION, *TARGET.POSITION):
                ATTACK, GAME_RUNNING = PLAYER.COMBAT_CHECK(TARGET)
                return GAME_RUNNING, POSITION
            else:
                print("TARGET is too far away.")

        else:
            print("Invalid TARGET. Enter the ID of the mob you want to attack.")
    except ValueError:
        print("Invalid TARGET. Enter the ID of the mob you want to attack.")
    except IndexError:
        print("Invalid TARGET. Enter the ID of the mob you want to attack.")


def USE_ITEM(PLAYER, COMMAND):
    PARTS = COMMAND.split()
    try:
        ITEM_ID = int(PARTS[1])
        if ITEMS[ITEM_ID]:
            ITEM = ITEMS[ITEM_ID]
            if ITEM in PLAYER.INVENTORY["ITEMS"]:
                if isinstance(ITEM, MELEE_WEAPON):
                    WEAPON = PLAYER.INVENTORY["WEAPON"]
                    if WEAPON:
                        PLAYER.INVENTORY["ITEMS"].append(WEAPON)
                    PLAYER.INVENTORY["WEAPON"] = ITEM
                    PLAYER.INVENTORY["ITEMS"].remove(ITEM)
                    print(f"Equipped {ITEM.NAME}.")
                else:
                    print(f"{ITEM.NAME} has no use.")
            else:
                print(f"ITEM.{ITEM_ID} not in INVENTORY.")
        else:
            print(f"ITEM.{ITEM_ID} not in INVENTORY.")
    except ValueError:
        print("Invalid ITEM. Enter the ID of the item you want to use.")
    except IndexError:
        print("Invalid ITEM. Enter the ID of the item you want to use.")


def PROCESS_COMMAND(PLAYER):
    POSITION = PLAYER.POSITION
    RETURN = None

    while True:  # Keep looping until a valid command is entered
        COMMAND = input(f"\n{PLAYER.NAME}, enter COMMAND: ").upper()  # Ask for a new command
        if COMMAND == "QUIT":
            return False, POSITION

        elif COMMAND.startswith(("NORTH", "SOUTH", "EAST", "WEST")):
            RETURN = MOVE_PLAYER(PLAYER, COMMAND)

        elif COMMAND.startswith("USE"):
            USE_ITEM(PLAYER, COMMAND)

        elif COMMAND == "LOOK":
            RETURN = True, POSITION
        
        elif COMMAND == "INVENTORY":
            OPEN_INVENTORY(PLAYER)

        elif COMMAND.startswith("ATTACK"):
            RETURN = ATTACK(PLAYER, COMMAND)

        elif COMMAND == "HELP":
            print("The objective is to escape the dungeon without being killed by the monsters.")
            print("To move, enter NORTH, SOUTH, EAST, or WEST and the number of feet you want to move.")
            print("To pass, enter LOOK.")
            print("To open inventory, enter INVENTORY.")
            print("To attack a monster, enter ATTACK.")
            print("To exit the game, enter QUIT.")
            print("For help, enter HELP.")

        else:
            print("Invalid COMMAND. Try again.")
        
        if RETURN:
            return RETURN
