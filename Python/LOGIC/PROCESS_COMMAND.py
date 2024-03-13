from WORLD.GLOBAL import MOBS, ITEMS
from ENTITIES.ITEMS.MELEE_WEAPONS.MELEE_WEAPON import MELEE_WEAPON
from ENTITIES.ITEMS.ARMOR.ARMOR import ARMOR
from LOGIC.MATH import MELEE_RANGE
from LOGIC.MATH import DISTANCE as MATH_DISTANCE
from WORLD.GLOBAL import GLOBAL_FLAGS
from WORLD.LOCATIONS.LOCATION_ID import LOCATION_ID

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


def MOVE_PLAYER(PLAYER, COMMAND, MOVEMENT):
    global GLOBAL_FLAGS
    DEBUG = GLOBAL_FLAGS["DEBUG"]
    COMBAT = GLOBAL_FLAGS["COMBAT"]
    if DEBUG:
        logging.debug(f"MOVE PLAYER COMBAT: {COMBAT}")
    PARTS = COMMAND.split()
    try:
        DIRECTION = PARTS[0]
        if len(PARTS) > 1:
            DISTANCE = int(PARTS[1])
            if DEBUG:
                logging.debug(f"DISTANCE: {DISTANCE}")
            if DISTANCE % 5 == 0:    
                DISTANCE = int(DISTANCE/5)
                # print(DISTANCE)
                if COMBAT:
                    DISTANCE = min(DISTANCE, PLAYER.SPEED)
                    if DEBUG:
                        logging.debug(DISTANCE)
            else:
                print("Invalid DISTANCE. DISTANCE must be divisible by 5.")
                return None
        else:
            DISTANCE = 1

        POSITION = PLAYER.MOVE(DIRECTION, DISTANCE)
        if POSITION == PLAYER.POSITION[0:2]:
            print("There is a wall in your path.")
        else:
            _DISTANCE = int(MATH_DISTANCE(*POSITION, *PLAYER.POSITION[0:2])*5)
            print(f"Moved {_DISTANCE} feet {DIRECTION}.")
            TEMP_X, TEMP_Y = PLAYER.POSITION[0:2]
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
                    if mob and mob != PLAYER and MELEE_RANGE(*mob.POSITION[0:2], *TEMP_POSITION[0:2]):
                        MOB_CHECKS[index] = True
                    else:
                        MOB_CHECKS[index] = False
                    CHECK2 = MOB_CHECKS[index]

                    if CHECK1 and not CHECK2:
                        GAME_RUNNING = mob.COMBAT_CHECK(PLAYER)
                        if not GAME_RUNNING:
                            return False, POSITION, False
                TEMP_POSITION[COORDINATE] += CHANGE
            
            MOVEMENT = max(MOVEMENT-_DISTANCE, 0)
            return True, POSITION, MOVEMENT
    except ValueError:
        print("Invalid DISTANCE.")





def ATTACK(PLAYER, COMMAND):
    PARTS = COMMAND.split()
    try:
        TARGET_ID = int(PARTS[1])-1
        if 0 < TARGET_ID < len(MOBS):
            TARGET = MOBS[TARGET_ID]
            if not TARGET:
                print("Invalid TARGET. Enter the ID of the mob you want to attack.")    
            elif TARGET == PLAYER:
                print("You cannot attack yourself.")
            elif MELEE_RANGE(*PLAYER.POSITION[0:2], *TARGET.POSITION[0:2]):
                GAME_RUNNING = PLAYER.COMBAT_CHECK(TARGET)
                return GAME_RUNNING, False
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
                if isinstance(ITEM, ARMOR):
                    _ARMOR = PLAYER.INVENTORY["ARMOR"]
                    if _ARMOR:
                        PLAYER.INVENTORY["ITEMS"].append(_ARMOR)
                    PLAYER.INVENTORY["ARMOR"] = ITEM
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


def _CONTAINER(PLAYER, COMMAND):
    PARTS = COMMAND.split()
    PLAYER_XY = PLAYER.POSITION[0:2]
    _LOCATION = LOCATION_ID(*PLAYER.POSITION[0:2])
    _COUNT = 0
    
    for ITEM in _LOCATION.LOCAL_ITEMS:
        if ITEM.TYPE in ["CHEST"] and MELEE_RANGE(*PLAYER_XY, *ITEM.POSITION[0:2]):
            _COUNT+=1
            container = ITEM
            break
        else:
            print(f"{ITEM.NAME} out of range.")
    
    if not _COUNT:
        print(f"No CONTAINER in {_LOCATION.DESCRIPTION}.")
        return

    _OPEN = container.OPEN
    if len(PARTS) == 1:
        if _OPEN:
            container.VIEW_CONTENTS()
        else:
            print(f"{container.NAME} is CLOSED.")
    elif PARTS[1] == "OPEN":
        if _OPEN:
            print(f"{container.NAME} is already open.")
        else:
            container.OPEN = True
            print(f"Opened {container.NAME}:")
            container.VIEW_CONTENTS()
    elif PARTS[1] == "CLOSE":
        if _OPEN:
            container.OPEN = False
            print(f"Closed {container.NAME}.")
        else:
            print(f"{container.NAME} is already closed.")
    elif PARTS[1] == "GOLD":
        if not _OPEN:
            print(f"{container.NAME} is closed.")
        elif container.GOLD:
            PLAYER.INVENTORY["GOLD"] += container.GOLD
            print(f"Took {container.GOLD} GOLD from {container.NAME}.")
            container.GOLD = 0
        elif len(PARTS) == 2:
            container.GOLD = PLAYER.INVENTORY["GOLD"]
            PLAYER.INVENTORY["GOLD"] = 0
            print(f"Stored {container.GOLD} in {container.NAME}.")
        else:
            _GOLD = min(float(PARTS[2]), PLAYER.INVENTORY["GOLD"])
            container.GOLD = _GOLD
            PLAYER.INVENTORY["GOLD"] -= _GOLD
            print(f"Stored {_GOLD} in {container.NAME}.")


    elif isinstance(int(PARTS[1]), int):
        if not _OPEN:
            print(f"{container.NAME} is closed.")
        else:
            ID = int(PARTS[1])
            if 0 <= ID < len(ITEMS):
                ITEM = ITEMS[ID]
                if ITEM in container.CONTENTS:
                    PLAYER.INVENTORY["ITEMS"].append(ITEM)
                    container.CONTENTS.remove(ITEM)
                    print(f"Added {ITEM.NAME} to INVENTORY.")
            else:
                print(f"ITEM not in {container.NAME}.")


def PROCESS_COMMAND(*args):
    global GLOBAL_FLAGS
    COMBAT = GLOBAL_FLAGS["COMBAT"]
    DEBUG = GLOBAL_FLAGS["DEBUG"]
    if DEBUG:
        logging.debug(f"PROCESS COMMAND COMBAT: {COMBAT}")
    PLAYER, ACTION, MOVEMENT = args
    POSITION = PLAYER.POSITION[0:2]
    RETURN = None


    while True:  # Keep looping until a valid command is entered
        COMMAND = input(f"\n{PLAYER.NAME}, enter COMMAND: ").upper()  # Ask for a new command
        X = None
        if COMMAND == "QUIT":
            return False, POSITION, False, False

        elif COMMAND.startswith(("NORTH", "SOUTH", "EAST", "WEST")):
            if MOVEMENT or not COMBAT:
                X = MOVE_PLAYER(PLAYER, COMMAND, MOVEMENT)
                if X:
                    GAME_RUNNING, POSITION, MOVEMENT = X
                    RETURN = GAME_RUNNING, POSITION, ACTION, MOVEMENT
            elif ACTION:
                INPUT = input("MOVEMENT exhausted. Use ACTION to DASH? ")
                if INPUT.upper() == "YES":
                    X = MOVE_PLAYER(PLAYER, COMMAND, ACTION)
                if X:
                    GAME_RUNNING, POSITION, ACTION = X
                    RETURN = GAME_RUNNING, POSITION, ACTION, MOVEMENT
            else:
                logging.error("MOVEMENT exhausted.")

        elif COMMAND.startswith("USE"):
            USE_ITEM(PLAYER, COMMAND)

        elif COMMAND == "LOOK":
            RETURN = True, POSITION, False, False
        
        elif COMMAND == "INVENTORY":
            OPEN_INVENTORY(PLAYER)

        elif COMMAND.startswith("ATTACK"):
            if ACTION == PLAYER.SPEED*5:
                X = ATTACK(PLAYER, COMMAND)
                if X:
                    GAME_RUNNING, ACTION = X
                    RETURN = GAME_RUNNING, POSITION, ACTION, MOVEMENT
            else:
                print("ACTION used. Make MOVEMENT.")

        elif COMMAND == "HELP":
            print("The objective is to escape the dungeon without being killed by the monsters.")
            print("To move, enter NORTH, SOUTH, EAST, or WEST and the number of feet you want to move.")
            print("To pass, enter LOOK.")
            print("To open inventory, enter INVENTORY.")
            print("To attack a monster, enter ATTACK.")
            print("To exit the game, enter QUIT.")
            print("For help, enter HELP.")
        
        elif COMMAND.startswith("CONTAINER"):
            _CONTAINER(PLAYER, COMMAND)

        else:
            print("Invalid COMMAND. Try again.")
        
        if RETURN:
            return RETURN
